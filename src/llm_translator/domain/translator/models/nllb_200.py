from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from .model_base import ModelBase


class NLLBModel(ModelBase):
    def __init__(self):
        model_name = "facebook/nllb-200-distilled-1.3B"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.src_lang = "jpn_Jpan"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        if torch.cuda.is_available():
            self.model.to("cuda")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    def _get_optimal_batch_size(self) -> int:
        """GPU メモリに基づいて最適なバッチサイズを決定"""
        if not torch.cuda.is_available():
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

    def cleanup(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()

    def translate(self, texts: list[str]) -> list[str]:
        results: list[str] = []
        batch_size = self._get_optimal_batch_size()

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # バッチ処理用の入力準備
            inputs = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )

            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}

            with torch.no_grad():
                translated_tokens = self.model.generate(
                    **inputs,
                    forced_bos_token_id=self.tokenizer.convert_tokens_to_ids(
                        "eng_Latn"
                    ),
                    max_length=200,
                    num_beams=4,
                    early_stopping=True,
                )

            batch_results = self.tokenizer.batch_decode(
                translated_tokens, skip_special_tokens=True
            )
            results.extend(batch_results)

        return results
