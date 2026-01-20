import os
from transformers import pipeline
import torch

from .IModel import IModel
from huggingface_hub import login


login(token=os.getenv("HUGGING_FACE_API_KEY"))


class GemmaModel(IModel):
    def __init__(self):
        self.pipe = pipeline(
            "image-text-to-text",
            model="google/translategemma-4b-it",
            device="cuda" if torch.cuda.is_available() else "cpu",
            dtype=torch.bfloat16,
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
        # translategemma-4bの場合、1サンプルあたり約100-200MBと想定
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
        def format_dataset(text: str):
            return [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "source_lang_code": "ja-JP",
                            "target_lang_code": "en",
                            "text": text,
                        }
                    ],
                }
            ]

        return [
            output[0]["generated_text"][-1]["content"].strip()
            for output in self.pipe(
                text=[format_dataset(text) for text in texts],  # type: ignore
                max_new_tokens=200,
                batch_size=self.batch_size,
            )
        ]
