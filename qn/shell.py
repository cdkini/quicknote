import pathlib
import subprocess
from typing import List, Tuple

import pyfzf


class Shell:

    FZF_OPTS = '--preview "bat --style=numbers --color=always --line-range :500 {}"'

    def __init__(self, editor: str) -> None:
        self._editor = editor
        self._fzf = pyfzf.pyfzf.FzfPrompt()

    def open(self, paths: List[pathlib.Path]) -> None:
        command = [self._editor]
        for path in paths:
            str_path = path.as_posix()
            command.append(str_path)

        subprocess.call(command)

    def fzf(self, paths: List[pathlib.Path]) -> Tuple[str, ...]:
        choices = [path.absolute().as_posix() for path in paths]
        results = self._fzf.prompt(choices, Shell.FZF_OPTS)
        return tuple(results)