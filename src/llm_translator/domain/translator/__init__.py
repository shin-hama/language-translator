from logging import Logger
from typing import Optional


class Translator:
    def __init__(self, logger: Optional[Logger]):
        # model ファイルの読み込みに時間がかかるのでここで初期化する
        # from .models.mbart import MbartModel
        from .models.gemma import GemmaModel

        if logger is not None:
            logger.info("Initialize Translator...")
        self.model = GemmaModel()

        if logger is not None:
            logger.info("Translator initialized.")

    def translate(self, texts: list[str]) -> list[str]:
        return self.model.translate(texts)
