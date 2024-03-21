from .models.mbart import MbartModel


class Translator:
    def __init__(self):
        self.model = MbartModel()

    def translate(self, text: str) -> str:
        return self.model.translate(text)
