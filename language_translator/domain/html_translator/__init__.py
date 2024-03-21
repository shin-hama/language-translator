from pathlib import Path
from domain.translator import Translator
from bs4 import BeautifulSoup


class HtmlTranslator:
    def __init__(self, translator: Translator):
        self.translator = translator
        pass

    def translate(self, file: Path) -> str:
        with open(file, mode="r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        # Find all text elements in the HTML
        for element in set(
            [
                elm
                for elm in soup.find_all(
                    ["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"]
                )
                if elm.get_text().strip() != ""
            ]
        ):
            content = element.get_text().strip()
            print(f"ja: {content}")
            print("------------" * 2)
            translated = self.translator.translate(content)
            print(f"en: {translated}")
            # content.replace_with(processed_text)
            print("============" * 2)
        return ""
