import pathlib


class Repo:
    def __init__(self, root: pathlib.Path):
        self._root = root
