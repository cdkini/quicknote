import pathlib
import subprocess
from typing import List, Tuple

import pyfzf

from qn.utils import pushd


class Shell:

    FZF_OPTS = '--preview "bat --style=numbers --color=always --line-range :500 {}"'

    def __init__(self, editor: str = "nvim", grep_cmd: str = "rg") -> None:
        self._editor = editor
        self._grep = grep_cmd
        self._fzf = pyfzf.pyfzf.FzfPrompt()

    def open(self, paths: List[pathlib.Path]) -> None:
        command = [self._editor]
        for path in paths:
            str_path = path.as_posix()
            command.append(str_path)

        subprocess.call(command)

    def grep(self, directory: pathlib.Path, args: Tuple[str, ...]) -> None:
        command = [self._grep]
        for arg in args:
            command.append(arg)

        path = directory.as_posix()
        command.append(path)

        subprocess.call(command)

    def fzf(
        self, directory: pathlib.Path, paths: List[pathlib.Path]
    ) -> Tuple[str, ...]:
        with pushd(directory.as_posix()):
            choices = sorted(map(lambda p: p.name, paths))
            results = self._fzf.prompt(choices, Shell.FZF_OPTS)
        return tuple(results)

    def user_confirmation(self, prompt: str) -> bool:
        answer = input(prompt)
        return answer.lower() in ("y", "yes")
