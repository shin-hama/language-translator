from typing import Any
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from .model_base import ModelBase


MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"


class MbartModel(ModelBase):
    def __init__(self):
        self.model: Any = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)

        self.tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_NAME)
        self.tokenizer.src_lang = "ja_XX"
        self.tokenizer.target_lang = "en_XX"

    def translate(self, texts: list[str]) -> list[str]:
        results: list[str] = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)

            translated = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[
                    self.tokenizer.target_lang
                ],
            )
            translated_text: list[str] = self.tokenizer.batch_decode(
                translated, skip_special_tokens=True
            )

            results.append(translated_text[0])

        return results
