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
            batch_size=64,
        )

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
                batch_size=64,
            )
        ]
