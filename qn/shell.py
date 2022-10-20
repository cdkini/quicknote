import datetime as dt
import pathlib
import subprocess
from typing import List, Tuple

import pyfzf

from qn.config import Config
from qn.utils import pushd


class Git:
    def __init__(self, root: pathlib.Path, remote_name: str) -> None:
        self._root = root
        self._remote_name = remote_name

    def add(self) -> None:
        with pushd(self._root.as_posix()):
            subprocess.call(["git", "add", "."])

    def commit(self) -> None:
        with pushd(self._root.as_posix()):
            subprocess.call(["git", "commit", "-m", dt.datetime.now().isoformat()])

    def push(self) -> None:
        with pushd(self._root.as_posix()):
            subprocess.call(["git", "push"])

    def status(self) -> None:
        with pushd(self._root.as_posix()):
            subprocess.call(["git", "status"])

    def get_url(self) -> str:
        with pushd(self._root.as_posix()):
            out = subprocess.check_output(
                ["git", "remote", "get-url", self._remote_name]
            )

        return out.decode("utf-8").strip()


class Shell:
    def __init__(self, root: pathlib.Path, config: Config) -> None:
        self._root = root
        self._editor = config.editor
        self._grep_cmd = config.grep_cmd
        self._git = Git(root=root, remote_name=config.git_remote_name)
        self._fzf_opts = config.fzf_opts

    @property
    def git(self) -> Git:
        return self._git

    def open_with_editor(self, paths: List[pathlib.Path]) -> None:
        command = [self._editor]
        for path in paths:
            str_path = path.as_posix()
            command.append(str_path)

        subprocess.call(command)

    def open_in_browser(self, url: str) -> None:
        subprocess.call(["open", url])

    def grep(self, args: Tuple[str, ...]) -> None:
        command = [self._grep_cmd]
        for arg in args:
            command.append(arg)

        path = self._root.as_posix()
        command.append(path)

        subprocess.call(command)

    def fzf(self, paths: List[pathlib.Path]) -> Tuple[str, ...]:
        fzf = pyfzf.pyfzf.FzfPrompt()
        with pushd(self._root.as_posix()):
            choices = sorted(map(lambda p: p.name, paths))
            results = fzf.prompt(choices, self._fzf_opts)
        return tuple(results)
