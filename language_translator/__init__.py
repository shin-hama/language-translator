from pathlib import Path
from domain.html_translator import HtmlTranslator
from domain.translator import Translator


if __name__ == "__main__":

    file = Path("samples/index.html")

    HtmlTranslator(Translator()).translate(file)
