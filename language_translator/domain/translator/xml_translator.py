from pathlib import Path
from domain.translator import Translator
from bs4 import BeautifulSoup
from tqdm import tqdm


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
            desc=soup.title.string if soup.title else None,
        ):
            text = node.get_text(strip=True)
            if not text:
                continue

            if not self._contains_japanese(text):
                continue

            translated = self.translator.translate(text)
            node.replace_with(translated.strip().replace("\n", ""))
        return soup.prettify()

    def _contains_japanese(self, text: str) -> bool:
        for character in text:
            if (
                "\u3040" <= character <= "\u309F"
                or "\u30A0" <= character <= "\u30FF"
                or "\u4E00" <= character <= "\u9FAF"
            ):
                return True
        return False
