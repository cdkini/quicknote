import pathlib
from typing import Tuple

from qn.editor import Editor


class Repo:
    def __init__(self, root: pathlib.Path, editor: Editor):
        self._root = root
        self._editor = editor

    def add_note(self, name: str) -> None:
        path = self._determine_path_from_name(name)
        if path.exists():
            raise ValueError(f"Note '{name}' already exists; please use 'qn open'")

        self._editor.open([path])

    def open_notes(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            raise NotImplementedError("FZF has not yet been implemented")

        paths = []
        for name in names:
            path = self._determine_path_from_name(name)
            if not path.exists():
                raise ValueError(f"Note '{name}' does not exist; please use 'qn add'")

            paths.append(path)

        self._editor.open(paths)

    def _determine_path_from_name(self, name: str) -> pathlib.Path:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        return path
