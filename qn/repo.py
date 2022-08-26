import pathlib

from qn.editor import Editor


class Repo:
    def __init__(self, root: pathlib.Path, editor: Editor):
        self._root = root
        self._editor = editor

    def add_note(self, name: str) -> None:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        if path.exists():
            raise ValueError(f"Note '{name}' already exists; please use 'qn open'")

        self._editor.open(path)
