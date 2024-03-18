class Translator:
    def __init__(self, language: str):
        self.language = language

    def translate(self, text: str) -> str:
        raise NotImplementedError(
            "This method should be implemented in the child class"
        )
