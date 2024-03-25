from logging import Logger
from pathlib import Path
from typing import Optional

from tqdm import tqdm
from domain.finder.html_finder import HtmlFinder
from domain.html_translator import HtmlTranslator
from domain.translator import Translator


def translate_html(root_dir: str | Path, logger: Optional[Logger]):
    """Translate HTML content from source language to target language."""
    html_parser = HtmlTranslator(Translator(logger))
    root_dir = Path(root_dir)

    for file in tqdm(HtmlFinder().find_all(root_dir), unit="files"):
        translated = html_parser.translate(file)

        # save translated text to file
        newFile = root_dir / "en" / file.relative_to(root_dir).parent
        newFile.mkdir(parents=True, exist_ok=True)

        newFile.write_text(translated)
