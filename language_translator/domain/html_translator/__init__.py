from .html_parser import HTMLParser
from pathlib import Path
from domain.translator import Translator
from bs4 import BeautifulSoup


class HtmlTranslator:
    def __init__(self, translator: Translator):
        self.translator = translator
        pass

    def translate(self, file: Path) -> str:
        parser = HTMLParser()
        with open(file, mode="r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        # Find all text elements in the HTML
        for content, element in {
            parser.parse(elm): elm
            for elm in soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "h6"])
        }.items():
            if (content) == "":
                continue
            translated = self.translator.translate(content)
            # print(f"ja: {content}")
            # print("------------" * 2)
            # print(f"en: {translated}")
            # print("============" * 2)
            parser.replace_parent_text(element, translated)
        return soup.prettify()
