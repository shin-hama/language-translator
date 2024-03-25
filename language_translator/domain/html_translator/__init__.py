from pathlib import Path
from domain.translator import Translator
from bs4 import BeautifulSoup
from tqdm import tqdm


class HtmlTranslator:
    def __init__(self, translator: Translator):
        self.translator = translator
        pass

    def translate(self, file: Path) -> str:
        with open(file, mode="r", encoding="utf-8-sig") as f:
            soup = BeautifulSoup(f, "html.parser")
        # Find all text elements in the HTML
        for node in tqdm(
            soup.find_all(text=True),
            leave=False,
            desc=soup.title.string if soup.title else None,
        ):
            if node.parent.name in ["script", "style", "[document]", "code"]:
                continue
            if not node.get_text(strip=True):
                continue

            translated = self.translator.translate(node.get_text(strip=True))
            node.replace_with(translated)
        return soup.prettify()
