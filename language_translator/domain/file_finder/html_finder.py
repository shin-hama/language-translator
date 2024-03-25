from pathlib import Path


class HtmlFinder:
    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)

    def get_all(self) -> list[Path]:
        return [
            file
            for file in self.root_dir.rglob("*.html")
            if not file.relative_to(self.root_dir).parts[0].startswith("en")
        ]
