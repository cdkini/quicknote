from __future__ import annotations

import difflib
import os
import pathlib
from typing import Dict, List, Optional, Tuple

import click

from qn.log import CommandLogger
from qn.shell import (
    fzf,
    git_add,
    git_commit,
    git_get_remote_url,
    git_push,
    git_status,
    grep,
    open_with_editor,
)


class Repo:

    ENV_VAR = "QN_ROOT"

    def __init__(self, root: pathlib.Path, logger: CommandLogger) -> None:
        self._root = root
        self._editor = os.environ.get("EDITOR", "vim")
        self._logger = logger

    @property
    def notes(self) -> Dict[str, pathlib.Path]:
        paths = list(
            filter(
                lambda n: n.is_file() and not n.stem.startswith("."),
                self._root.iterdir(),
            )
        )
        return {path.stem.lower(): path for path in paths}

    @classmethod
    def create(cls) -> Repo:
        root = cls._determine_root()
        logger = CommandLogger(root)
        return cls(root=root, logger=logger)

    @classmethod
    def _determine_root(cls) -> pathlib.Path:
        path = os.environ.get(cls.ENV_VAR)
        if path is None:
            raise ValueError(f"No value found for {cls.ENV_VAR} env var")

        root = pathlib.Path(path)
        if not root.exists():
            raise ValueError(f"{cls.ENV_VAR} '{path}' does not exist")
        if not root.is_dir():
            raise ValueError(f"{cls.ENV_VAR} '{path}' is not a directory")

        return root

    def chdir(self) -> None:
        os.chdir(self._root)

    def add(self, name: str, exists_ok: bool) -> None:
        if not exists_ok and name in self.notes:
            raise FileExistsError(f"'{name}' already exists")

        path = self._determine_path_from_name(name)
        open_with_editor(paths=[path], editor=self._editor)

    def open(self, names: Tuple[str, ...]) -> None:
        names = names or self._interactively_retrieve_names()
        paths = self._determine_paths_from_names(names=names)
        open_with_editor(paths=paths, editor=self._editor)

    def list(self, reverse: bool = False) -> List[str]:
        return sorted(self.notes.keys(), reverse=reverse)

    def delete(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        for path in paths:
            if click.confirm(f"Delete '{path.stem}'"):
                path.unlink()

    def grep(self, args: Tuple[str, ...]) -> None:
        grep(args=args)

    def status(self) -> None:
        git_status()

    def sync(self) -> None:
        git_add()
        git_commit()
        git_push()

    def web(self) -> None:
        url = git_get_remote_url()
        click.launch(url)

    def log(self) -> None:
        self._logger.log()

    def _interactively_retrieve_names(self) -> Tuple[str, ...]:
        paths = list(self.notes.values())
        names = fzf(
            paths=paths,
            preview_opts="bat --style=numbers --color=always --line-range :500 {}",
        )
        return names

    def _determine_paths_from_names(self, names: Tuple[str, ...]) -> List[pathlib.Path]:
        paths = []

        for name in names:
            path = self._determine_path_from_name(name)
            if not path.exists():
                path = self._determine_closest_path_from_name(name)
            paths.append(path)

        return paths

    def _determine_path_from_name(self, name: str) -> pathlib.Path:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        return path

    def _determine_closest_path_from_name(self, name: str) -> pathlib.Path:
        closest_name = self._find_closest_name(name)
        if closest_name is None:
            raise FileNotFoundError(f"'{name}' does not exist")

        return self._determine_path_from_name(closest_name)

    def _find_closest_name(self, name: str) -> Optional[str]:
        name = name.lower()
        names = [name.lower() for name in self.notes.keys()]
        matches = difflib.get_close_matches(name, names)
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        return self._user_choice(matches)

    @staticmethod
    def _user_choice(choices: List[str]) -> str:
        for i, choice in enumerate(choices):
            print(f"{i+1}: {choice}")

        selection = int(input("Choice: "))

        return choices[selection - 1]
