from pathlib import Path


class FileFinder:
    def __init__(self, root_dir: str | Path, exts: str | list[str] = "*"):
        self.root_dir = Path(root_dir)
        self.patterns: list[str] = [exts] if isinstance(exts, str) else exts

    def get_all(self) -> list[Path]:
        return [
            file
            for pattern in self.patterns
            for file in self.root_dir.rglob(pattern)
            if not file.relative_to(self.root_dir).parts[0].startswith("en")
        ]
