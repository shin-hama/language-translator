from logging import Logger
from typing import Optional
from .models.mbart import MbartModel


class Translator:
    def __init__(self, logger: Optional[Logger]):
        if logger is not None:
            logger.info("Initialize Translator...")
        self.model = MbartModel()

    def translate(self, text: str) -> str:
        return self.model.translate(text).strip()
