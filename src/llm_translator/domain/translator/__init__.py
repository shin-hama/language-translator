from logging import Logger
from typing import Optional

from llm_translator.domain.translator.models.model_base import ModelBase


class Translator:
    def __init__(self, logger: Optional[Logger]):
        # model ファイルの読み込みに時間がかかるのでここで初期化する
        # from .models.mbart import MbartModel
        from .models.gemma import GemmaModel

        if logger is not None:
            logger.info("Initialize Translator...")
        self.model: ModelBase = GemmaModel()

        if logger is not None:
            logger.info("Translator initialized.")

    def translate(self, texts: list[str]) -> list[str]:
        return self.model.translate(texts)
