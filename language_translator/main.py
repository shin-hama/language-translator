from argparse import ArgumentParser
from logging import getLogger, StreamHandler, DEBUG

from application.translate_html import exec


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Translate HTML content from source language to target language."
    )
    parser.add_argument(
        "--root",
        type=str,
        help="Root directory containing HTML files to translate.",
        required=True,
    )
    args = parser.parse_args()
    exec(args.root, logger)
