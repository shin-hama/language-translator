import logging

import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from .model_base import ModelBase


logger = logging.getLogger(__name__)

MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"

# mBART の位置埋め込み上限。これ以上は入力も出力も扱えないので、
# 打ち切りは「モデルの構造上の限界」でのみ起こるようにする。
# (config の max_length=200 のままだと長い段落が黙って途中で切れる)
MODEL_MAX_LENGTH = 1024
MAX_INPUT_LENGTH = MODEL_MAX_LENGTH

# 出力上限は入力長に比例させる。日→英はトークン数が増えるので余裕を持たせつつ、
# 一律に大きな値を置くと暴走生成を最後まで走らせてしまうため。
OUTPUT_LENGTH_RATIO = 2
OUTPUT_LENGTH_MARGIN = 64

# 空きメモリ1GBあたり何トークン位置を処理できるかの見積り。
# 実測 (fp16 / beam5) では VRAM 4GB 相当で 913 トークン x 4 件が 3.04GB だったので、
# それより安全側に倒した値にしている。
TOKENS_PER_GB = 1000
MEMORY_HEADROOM_GB = 0.5
# greedy(=1) は計算律速な GPU では約2倍速いが、段落末尾に同じ文を
# 生成する事例が 64件中2件あったため beam を維持する。
# no_repeat_ngram_size での抑制も試したが、言い換えを強制された結果
# 識別子(ILogService や Plugins パス)が壊れるため使えない。
# なお beam 側にも逆の弱点があり、2文の段落で1文目を落とす事例がある
# (length_penalty を上げても回復しなかった)。速度向上は fp16 と
# バッチ化によるもので、この値の選択には依存しない。
NUM_BEAMS = 5


class MbartModel(ModelBase):
    def __init__(self):
        self.use_cuda = torch.cuda.is_available()

        self.model = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)
        if self.use_cuda:
            # T400 のような低帯域 GPU では fp16 で VRAM と帯域の消費が半減する。
            # CPU では fp16 が遅くなるので fp32 のままにする。
            # from_pretrained の dtype 引数は transformers 4.56 以降にしか無く、
            # pyproject が許容する 4.37 では動かないので .half() で変換する。
            self.model = self.model.half().to("cuda")  # type: ignore
        self.model.eval()  # type: ignore

        self.tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_NAME)
        self.tokenizer.src_lang = "ja_XX"
        self.tokenizer.target_lang = "en_XX"
        # lang_code_to_id は deprecated なので convert_tokens_to_ids を使う
        self.target_bos_token_id = self.tokenizer.convert_tokens_to_ids(
            self.tokenizer.target_lang
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    def _get_optimal_batch_size(self) -> int:
        """GPU メモリに基づいて最適なバッチサイズを決定"""
        if not self.use_cuda:
            return 1

        # モデルロード後の空きメモリを確認（より正確）
        free_memory_gb = torch.cuda.mem_get_info()[0] / 1024**3

        # 空きメモリに基づいてバッチサイズを決定
        if free_memory_gb < 2:
            return 4
        elif free_memory_gb < 4:
            return 8
        elif free_memory_gb < 8:
            return 16
        elif free_memory_gb < 12:
            return 32
        elif free_memory_gb < 20:
            return 64
        else:
            return 128

    def _get_token_budget(self) -> int:
        """1バッチで扱えるトークン位置数の上限。

        使用メモリは「件数 × バッチ内最長トークン数」に比例するため、
        件数だけで決めると長い段落で OOM する
        (VRAM 4GB で 900 トークン級を 8 件まとめると溢れることを確認済み)。
        """
        if not self.use_cuda:
            return MAX_INPUT_LENGTH

        free_memory_gb = torch.cuda.mem_get_info()[0] / 1024**3
        budget = int((free_memory_gb - MEMORY_HEADROOM_GB) * TOKENS_PER_GB)
        # 1件だけは必ず処理できるようにする
        return max(MAX_INPUT_LENGTH, budget)

    def _make_batches(self, lengths: list[int]) -> list[tuple[int, int]]:
        """件数上限とトークン上限の両方を満たす [開始, 終了) の並びを作る。

        呼び出し側が zip で対応付けるため、入力順は変えない。
        """
        max_items = self._get_optimal_batch_size()
        budget = self._get_token_budget()

        batches: list[tuple[int, int]] = []
        start = 0
        longest = 0
        for i, length in enumerate(lengths):
            candidate_longest = max(longest, length)
            n = i - start + 1
            if start < i and (n > max_items or candidate_longest * n > budget):
                batches.append((start, i))
                start, longest = i, length
            else:
                longest = candidate_longest
        if start < len(lengths):
            batches.append((start, len(lengths)))
        return batches

    def cleanup(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()

    def _generate(self, batch_texts: list[str]) -> list[str]:
        inputs = self.tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=MAX_INPUT_LENGTH,
        )

        max_new_tokens = min(
            MODEL_MAX_LENGTH,
            inputs["input_ids"].shape[1] * OUTPUT_LENGTH_RATIO + OUTPUT_LENGTH_MARGIN,
        )

        if self.use_cuda:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        with torch.no_grad():
            translated = self.model.generate(
                **inputs,
                forced_bos_token_id=self.target_bos_token_id,
                max_new_tokens=max_new_tokens,
                num_beams=NUM_BEAMS,
            )

        return self.tokenizer.batch_decode(translated, skip_special_tokens=True)

    def _generate_with_retry(self, batch_texts: list[str]) -> list[str]:
        """見積りが外れて OOM したらバッチを半分にして再試行する保険。"""
        try:
            return self._generate(batch_texts)
        except torch.cuda.OutOfMemoryError:
            if len(batch_texts) == 1:
                raise

        # 解放と再試行は except 節を抜けてから行う。
        # except 節の中では例外の traceback が失敗時のテンソルを掴んだままなので、
        # そこで cleanup() してもメモリが返らず分割しても OOM が続く。
        logger.warning(
            "%d 件のバッチで GPU メモリが不足したため分割して再試行します",
            len(batch_texts),
        )
        self.cleanup()
        half = len(batch_texts) // 2
        return self._generate_with_retry(
            batch_texts[:half]
        ) + self._generate_with_retry(batch_texts[half:])

    def translate(self, texts: list[str]) -> list[str]:
        if not texts:
            return []

        # 長さの取得と打ち切り警告をまとめて行う（打ち切りは訳文の欠落になるため）
        lengths: list[int] = []
        for text, ids in zip(
            texts, self.tokenizer(texts, truncation=False)["input_ids"]
        ):
            if len(ids) > MAX_INPUT_LENGTH:
                logger.warning(
                    "入力が %d トークンでモデル上限 %d を超えるため末尾を切り捨てます: %s...",
                    len(ids),
                    MAX_INPUT_LENGTH,
                    text[:60],
                )
            lengths.append(min(len(ids), MAX_INPUT_LENGTH))

        # 入力順に1件1件対応した結果を返す（呼び出し側が zip で対応付けるため）
        results: list[str] = []
        for start, end in self._make_batches(lengths):
            results.extend(self._generate_with_retry(texts[start:end]))

        return results
