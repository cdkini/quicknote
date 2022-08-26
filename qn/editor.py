import pathlib
import subprocess


class Editor:
    def __init__(self, cmd: str) -> None:
        self._cmd = cmd

    def open(self, path: pathlib.Path) -> None:
        subprocess.call([self._cmd, path.as_posix()])
