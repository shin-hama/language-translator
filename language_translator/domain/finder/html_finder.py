from pathlib import Path
from collections.abc import Iterator


class HtmlFinder:
    def __init__(self):
        pass

    def find_all(self, root_dir: Path | str = Path.cwd()) -> Iterator[Path]:
        if isinstance(root_dir, str):
            root_dir = Path(root_dir)

        return root_dir.rglob("*.html")
