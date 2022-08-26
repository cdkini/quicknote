import pathlib
import subprocess
from typing import List


class ShellManager:
    def __init__(self, editor: str) -> None:
        self._editor = editor

    def open(self, paths: List[pathlib.Path]) -> None:
        command = [self._editor]
        for path in paths:
            str_path = path.as_posix()
            command.append(str_path)

        subprocess.call(command)
