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

    def translate_text(self, text: str) -> str:
        """Translate text from source language to target language."""
        translator = Translator(self.logger)
        return translator.translate([text])[0]

    def translate_file(self, file_path: str) -> None:
        """Translate HTML content from source language to target language."""
        if self.logger is not None:
            self.logger.info(f"Start translate files {file_path}")

        translator = Translator(self.logger)

        file = Path(file_path)
        translated = self._translate_file(file, translator)
        if translated is None:
            return

        self._save_translated_file(
            Path(file_path).with_suffix(f".en{file.suffix}"), translated
        )

    def translate_files(self, root_dir: str) -> None:
        """Translate HTML content from source language to target language."""
        root = Path(root_dir)

        if self.logger is not None:
            self.logger.info(f"Start translate files in {root}")

        translator = Translator(self.logger)

        for file in tqdm(FileFinder(root, ["*.html", "*.xml"]).get_all(), unit="files"):
            translated = self._translate_file(file, translator)
            if translated is None:
                continue

            # save translated text to file
            new_file = root.parent / f"{root.name}.en" / file.relative_to(root)
            self._save_translated_file(new_file, translated)

    def _translate_file(self, file: Path, translator: Translator) -> str | None:
        """Translate text from source language to target language."""
        if file.suffix == ".html":
            return HtmlTranslator(translator).translate(file)
        elif file.suffix == ".xml":
            return XmlTranslator(translator).translate(file)
        else:
            print(f"Unsupported file type: {file.name}")
            return None

    def _save_translated_file(self, new_file: Path, translated: str) -> None:
        """Save translated text to file."""
        new_file.parent.mkdir(parents=True, exist_ok=True)

        new_file.write_text(translated, encoding="utf-8")
