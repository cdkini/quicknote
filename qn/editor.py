import pathlib
import subprocess


class Editor:
    def __init__(self, cmd: str):
        self._cmd = cmd

    def open(self, path: pathlib.Path):
        subprocess.call([self._cmd, path.as_posix()])
