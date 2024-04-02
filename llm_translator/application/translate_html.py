from logging import Logger
from pathlib import Path
from typing import Optional

from tqdm import tqdm
from llm_translator.domain.html_translator import HtmlTranslator
from llm_translator.domain.translator import Translator
from llm_translator.domain.file_finder.html_finder import HtmlFinder


def exec(root_dir: str | Path, logger: Optional[Logger]):
    """Translate HTML content from source language to target language."""
    html_parser = HtmlTranslator(Translator(logger))
    root_dir = Path(root_dir)

    if logger is not None:
        logger.info(f"Start translate html files in {root_dir}")
    for file in tqdm(HtmlFinder(root_dir).get_all(), unit="files"):
        translated = html_parser.translate(file)

        # save translated text to file
        newFile = root_dir / "en" / file.relative_to(root_dir)
        newFile.parent.mkdir(parents=True, exist_ok=True)

        newFile.write_text(translated, encoding="utf-8")
