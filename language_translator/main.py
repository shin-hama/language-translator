from application.translate_html import exec
from logging import getLogger, StreamHandler, DEBUG

from pathlib import Path

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    exec(project_root / "samples", logger)
