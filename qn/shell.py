import datetime as dt
import pathlib
import subprocess
from typing import List, Tuple

import pyfzf


def git_add() -> None:
    subprocess.call(["git", "add", "."])


def git_commit() -> None:
    subprocess.call(["git", "commit", "-m", dt.datetime.now().isoformat()])


def git_push() -> None:
    subprocess.call(["git", "push"])


def git_status() -> None:
    subprocess.call(["git", "status"])


def git_get_remote_url(remote_name: str) -> str:
    out = subprocess.check_output(["git", "remote", "get-url", remote_name])
    return out.decode("utf-8").strip()


def open_with_editor(paths: List[pathlib.Path], editor: str) -> None:
    command = [editor]
    for path in paths:
        str_path = path.as_posix()
        command.append(str_path)
    subprocess.call(command)


def open_in_browser(url: str) -> None:
    subprocess.call(["open", url])


def grep(args: Tuple[str, ...], grep_cmd: str) -> None:
    command = [grep_cmd]
    for arg in args:
        command.append(arg)
    subprocess.call(command)


def fzf(paths: List[pathlib.Path], fzf_opts: str) -> Tuple[str, ...]:
    fzf = pyfzf.pyfzf.FzfPrompt()
    choices = sorted(map(lambda p: p.name, paths))
    results = fzf.prompt(choices, fzf_opts)
    return tuple(results)
