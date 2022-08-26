import pathlib
import subprocess
from typing import List


class Editor:
    def __init__(self, cmd: str) -> None:
        self._cmd = cmd

    def open(self, paths: List[pathlib.Path]) -> None:
        command = [self._cmd]
        for path in paths:
            str_path = path.as_posix()
            command.append(str_path)

        subprocess.call(command)
