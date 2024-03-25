from logging import getLogger, StreamHandler, DEBUG

from pathlib import Path
from domain.html_translator import HtmlTranslator
from domain.translator import Translator

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


if __name__ == "__main__":
    logger.info("Start translation sample")
    root_dir = Path("./samples")
    file = Path(root_dir / "_index.html")

    result = HtmlTranslator(Translator(logger)).translate(file)

    # save translated text to file
    newFile = root_dir / "en" / file.relative_to(root_dir)
    newFile.parent.mkdir(parents=True, exist_ok=True)

    newFile.write_text(result, encoding="utf-8")
