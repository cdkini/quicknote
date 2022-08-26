import os
import pathlib


class Repo:
    def __init__(self, root: pathlib.Path):
        self._root = root

    @classmethod
    def create(cls) -> "Repo":
        path = os.environ.get("QN_ROOT")
        if path is None:
            raise ValueError("No value found for QN_ROOT env var")

        root = pathlib.Path(path)
        if not root.exists():
            raise ValueError(f"QN_ROOT '{path}' does not exist")
        if not root.is_dir():
            raise ValueError(f"QN_ROOT '{path}' is not a directory")

        return cls(root=root)
