import fire
from logging import getLogger, StreamHandler, DEBUG

from llm_translator.application.translate_html import exec


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def main(root: str):
    exec(root, logger)


if __name__ == "__main__":
    fire.Fire(main)
