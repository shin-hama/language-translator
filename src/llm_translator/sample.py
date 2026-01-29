from logging import getLogger, StreamHandler, DEBUG

from dotenv import load_dotenv
from pathlib import Path
from llm_translator.domain.html_translator import HtmlTranslator
from llm_translator.domain.translator import Translator


load_dotenv()  # .envファイルを読み込む

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


if __name__ == "__main__":
    logger.info("Start translation sample")
    root_dir = Path("./samples")
    file = Path(root_dir / "index.html")

    result = HtmlTranslator(Translator(logger)).translate(file)

    # save translated text to file
    newFile = root_dir / "en" / file.relative_to(root_dir)
    newFile.parent.mkdir(parents=True, exist_ok=True)

    newFile.write_text(result, encoding="utf-8")

    # result = Translator(logger).translate(["これは日本語の文章です。"])
    # print(result)
