import datetime as dt
import pathlib
import subprocess
from typing import List, Tuple

import pyfzf

from qn.utils import pushd


def open_with_editor(editor: str, paths: List[pathlib.Path]) -> None:
    command = [editor]
    for path in paths:
        str_path = path.as_posix()
        command.append(str_path)

    subprocess.call(command)


def open_in_browser(url: str) -> None:
    subprocess.call(["open", url])


def grep(cmd: str, directory: pathlib.Path, args: Tuple[str, ...]) -> None:
    command = [cmd]
    for arg in args:
        command.append(arg)

    path = directory.as_posix()
    command.append(path)

    subprocess.call(command)


def fzf(
    directory: pathlib.Path, paths: List[pathlib.Path], opts: str = ""
) -> Tuple[str, ...]:
    fzf = pyfzf.pyfzf.FzfPrompt()
    with pushd(directory.as_posix()):
        choices = sorted(map(lambda p: p.name, paths))
        results = fzf.prompt(choices, opts)
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


def git_get_url(directory: pathlib.Path, remote_name: str) -> str:
    with pushd(directory.as_posix()):
        out = subprocess.check_output(["git", "remote", "get-url", remote_name])

    return out.decode("utf-8").strip()
