from logging import Logger
from typing import Optional


class Translator:
    def __init__(self, logger: Optional[Logger]):
        # model ファイルの読み込みに時間がかかるのでここで初期化する
        from .models.mbart import MbartModel

        if logger is not None:
            logger.info("Initialize Translator...")
        self.model = MbartModel()

    def translate(self, text: str) -> str:
        return self.model.translate(text).strip()
