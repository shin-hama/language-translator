from pathlib import Path
from domain.finder.html_finder import HtmlFinder
from domain.html_translator import HtmlTranslator
from domain.translator import Translator


def translate_html(root_dir: str | Path, source_language, target_language):
    """Translate HTML content from source language to target language."""
    root_dir = Path(root_dir)

    translator = Translator(source_language)
    html_parser = HtmlTranslator(translator)

    for file in HtmlFinder().find_all(root_dir):
        translated = html_parser.translate(file)

        # save translated text to file
        newFile = root_dir / "target_language" / file.relative_to(root_dir).parent
        newFile.mkdir(parents=True, exist_ok=True)

        newFile.write_text(translated)
