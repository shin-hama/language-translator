from logging import Logger
from pathlib import Path
from typing import Optional

from tqdm import tqdm

from llm_translator.domain.html_translator import HtmlTranslator
from llm_translator.domain.translator import Translator
from llm_translator.domain.file_finder.html_finder import FileFinder
from llm_translator.domain.translator.xml_translator import XmlTranslator


class TranslateService:
    def __init__(self, logger: Optional[Logger]):
        self.logger = logger
        pass

    def translate_text(self, text: str) -> str:
        """Translate text from source language to target language."""
        translator = Translator(self.logger)
        return translator.translate(text)

    def translate_files(self, root_dir: str) -> None:
        """Translate HTML content from source language to target language."""
        translator = Translator(self.logger)

        root = Path(root_dir)

        if self.logger is not None:
            self.logger.info(f"Start translate files in {root}")

        for file in tqdm(FileFinder(root, ["*.html", "*.xml"]).get_all(), unit="files"):
            if file.suffix == ".html":
                translated = HtmlTranslator(translator).translate(file)
            elif file.suffix == ".xml":
                translated = XmlTranslator(translator).translate(file)
            else:
                print(f"Unsupported file type: {file.name}")
                continue

            # save translated text to file
            newFile = root / "en" / file.relative_to(root)
            newFile.parent.mkdir(parents=True, exist_ok=True)

            newFile.write_text(translated, encoding="utf-8")
