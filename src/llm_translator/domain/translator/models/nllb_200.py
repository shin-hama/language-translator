import os
from transformers import pipeline
import torch

from .model_base import ModelBase
from huggingface_hub import login


login(token=os.getenv("HUGGING_FACE_API_KEY"))


class NLLBModel(ModelBase):
    def __init__(self):
        self.pipe = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-1.3B",
            src_lang="jpn_Jpan",
            tgt_lang="eng_Latn",
            device="cuda" if torch.cuda.is_available() else "cpu",
            dtype=torch.float16,
        )
        self.batch_size = self._get_optimal_batch_size()

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
        if hasattr(self, "pipe"):
            del self.pipe

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()

    def translate(self, texts: list[str]) -> list[str]:
        return [
            output["translation_text"]
            for output in self.pipe(
                [text for text in texts],
                max_new_tokens=200,
                batch_size=self.batch_size,
            )
        ]
