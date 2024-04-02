from typing import Optional
import fire
from logging import getLogger, StreamHandler, DEBUG

from llm_translator.application import TranslateService


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def main(
    text: Optional[str] = None, file: Optional[str] = None, dir: Optional[str] = None
):
    service = TranslateService(logger)
    if text is not None:
        print(service.translate_text(text))
    elif file is not None:
        print("Not supported")
        # service.translate_file(file)
    elif dir is not None:
        service.translate_files(dir)
    else:
        print("Not supported")


if __name__ == "__main__":
    fire.Fire(main)
