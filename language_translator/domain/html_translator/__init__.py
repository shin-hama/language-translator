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
            # Find all elements in the HTML
        for element in soup.find_all():
            # Process the text of each element (convert all characters to uppercase as a sample)
            content = element.get_text()

            if content.strip() != "":
                # processed_text = self.translator.translate(content)
                # content.replace_with(processed_text)
                print(content)
                print("============" * 2)
        return ""
