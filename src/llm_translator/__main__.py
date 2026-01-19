"""
test
"""

from dotenv import load_dotenv
import fire
from logging import getLogger, StreamHandler, DEBUG
from importlib import metadata
from typing import Optional

from .application import TranslateService


load_dotenv()  # .envファイルを読み込む

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def main(
    text: Optional[str] = None,
    file: Optional[str] = None,
    dir: Optional[str] = None,
    version: bool = False,
):
    """
    Translate text or files from source Japanese to English.

    :param text: Text to translate.
    :param file: File to translate.
    :param dir: Directory to translate.
    :param version: Print version.
    """
    if version:
        print(metadata.version("llm_translator"))
        return

    service = TranslateService(logger)
    if text is not None:
        print(service.translate_text(text))
    elif file is not None:
        service.translate_file(file)
    elif dir is not None:
        service.translate_files(dir)
    else:
        print("Not supported")


if __name__ == "__main__":
    fire.Fire(main)
