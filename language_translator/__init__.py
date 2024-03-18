if __name__ == "__main__":
    from pathlib import Path
    from domain.html_translator import HtmlTranslator

    file = Path("samples/index.html")

    HtmlTranslator(None).translate(file)
