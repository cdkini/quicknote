import datetime as dt
import pathlib
import subprocess
from typing import List, Tuple

import pyfzf

from qn.utils import pushd

EDITOR = "nvim"
GREP_CMD = "rg"
FZF_OPTS = '-m --preview "bat --style=numbers --color=always --line-range :500 {}"'


def open_with_editor(paths: List[pathlib.Path]) -> None:
    command = [EDITOR]
    for path in paths:
        str_path = path.as_posix()
        command.append(str_path)

    subprocess.call(command)


def grep(directory: pathlib.Path, args: Tuple[str, ...]) -> None:
    command = [GREP_CMD]
    for arg in args:
        command.append(arg)

    path = directory.as_posix()
    command.append(path)

    subprocess.call(command)


def fzf(directory: pathlib.Path, paths: List[pathlib.Path]) -> Tuple[str, ...]:
    fzf = pyfzf.pyfzf.FzfPrompt()
    with pushd(directory.as_posix()):
        choices = sorted(map(lambda p: p.name, paths))
        results = fzf.prompt(choices, FZF_OPTS)
    return tuple(results)


def git_add(directory: pathlib.Path) -> None:
    with pushd(directory.as_posix()):
        subprocess.call(["git", "add", "."])


def git_commit(directory: pathlib.Path) -> None:
    with pushd(directory.as_posix()):
        subprocess.call(["git", "commit", "-m", dt.datetime.now().isoformat()])


def git_push(directory: pathlib.Path) -> None:
    with pushd(directory.as_posix()):
        subprocess.call(["git", "push"])


def git_status(directory: pathlib.Path) -> None:
    with pushd(directory.as_posix()):
        subprocess.call(["git", "status"])
