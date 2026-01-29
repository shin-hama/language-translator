import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from .model_base import ModelBase


MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"


class MbartModel(ModelBase):
    def __init__(self):
        self.model = MBartForConditionalGeneration.from_pretrained(MODEL_NAME)
        if torch.cuda.is_available():
            self.model.to("cuda")  # type: ignore

        self.tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_NAME)
        self.tokenizer.src_lang = "ja_XX"
        self.tokenizer.target_lang = "en_XX"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    def cleanup(self):
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc

        gc.collect()

    def translate(self, texts: list[str]) -> list[str]:
        results: list[str] = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)

            if torch.cuda.is_available():
                inputs = {k: v.to("cuda") for k, v in inputs.items()}

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
