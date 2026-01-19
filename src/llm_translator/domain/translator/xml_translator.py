from pathlib import Path
from bs4 import BeautifulSoup
from tqdm import tqdm

from llm_translator.domain.translator import Translator


class XmlTranslator:
    def __init__(self, translator: Translator):
        self.translator = translator
        pass

    def translate(self, file: Path) -> str:
        with open(file, mode="r", encoding="utf-8-sig") as f:
            soup = BeautifulSoup(f, "lxml-xml")
        # Find all text elements in the HTML
        for node in tqdm(
            soup.find_all(text=True),
            leave=False,
            desc=file.name,
        ):
            text = node.get_text(strip=True)
            if not text:
                continue

            if not self._contains_japanese(text):
                continue

            translated = self.translator.translate([text])
            node.replace_with(translated[0].replace("\n", ""))
        return soup.prettify()

    def _contains_japanese(self, text: str) -> bool:
        for character in text:
            if (
                "\u3040" <= character <= "\u309f"
                or "\u30a0" <= character <= "\u30ff"
                or "\u4e00" <= character <= "\u9faf"
            ):
                return True
        return False
