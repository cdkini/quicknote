from __future__ import annotations

import datetime as dt
import difflib
import os
import pathlib
from typing import Callable, Dict, List, Optional, Tuple

import qn.shell as shell
from qn.config import Config
from qn.log import CommandLogger
from qn.utils import Sorter, user_choice, user_confirmation


class Repo:

    ENV_VAR = "QN_ROOT"

    def __init__(
        self, root: pathlib.Path, logger: CommandLogger, config: Config
    ) -> None:
        self._root = root
        self._logger = logger
        self._config = config
        self._notes = self._init_notes()

    def _init_notes(self) -> Dict[str, pathlib.Path]:
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
        config = Config.parse_from_root(root)
        logger = CommandLogger(root)
        return cls(root=root, logger=logger, config=config)

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

    def add(self, name: str) -> None:
        if name in self._notes:
            raise FileExistsError(f"'{name}' already exists")

        path = self._determine_path_from_name(name)
        shell.open_with_editor(editor=self._config.editor, paths=[path])

    def open(self, names: Tuple[str, ...], sorter: Optional[Sorter] = None) -> None:
        if sorter:
            last = self.list(sorter=sorter)[-1]
            names = (last,)
        else:
            if len(names) == 0:
                names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        shell.open_with_editor(editor=self._config.editor, paths=paths)

    def put(self, name: str) -> None:
        path = self._determine_path_from_name(name)
        shell.open_with_editor(editor=self._config.editor, paths=[path])

    def daily(self) -> None:
        today = str(dt.date.today())
        self.put(today)

    def list(self, sorter: Sorter = Sorter.NAME, reverse: bool = False) -> List[str]:
        if sorter is Sorter.NAME:
            return sorted(self._notes.keys(), reverse=reverse)

        key_fn: Optional[Callable] = None
        if sorter is Sorter.CREATED:
            key_fn = lambda n: self._notes[n].stat().st_birthtime  # noqa: E731
        elif sorter is Sorter.MODIFIED:
            key_fn = lambda n: self._notes[n].stat().st_mtime  # noqa: E731
        elif sorter is Sorter.ACCESSED:
            key_fn = lambda n: self._notes[n].stat().st_atime  # noqa: E731

        assert key_fn is not None
        return sorted(self._notes, key=key_fn, reverse=reverse)

    def delete(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        for path in paths:
            confirmation = user_confirmation(f"Delete '{path.stem}' [y/n]: ")
            if confirmation:
                path.unlink()

    def grep(self, args: Tuple[str, ...]) -> None:
        shell.grep(cmd=self._config.grep_cmd, directory=self._root, args=args)

    def status(self) -> None:
        shell.git_status(self._root)

    def sync(self) -> None:
        shell.git_add(self._root)
        shell.git_commit(self._root)
        shell.git_push(self._root)

    def web(self) -> None:
        url = shell.git_get_url(
            directory=self._root, remote_name=self._config.git_remote_name
        )
        shell.open_in_browser(url)

    def log(self) -> None:
        self._logger.log()

    def _interactively_retrieve_names(self) -> Tuple[str, ...]:
        paths = list(self._notes.values())
        names = shell.fzf(self._root, paths, opts=self._config.fzf_opts)
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
        names = [name.lower() for name in self._notes.keys()]
        matches = difflib.get_close_matches(name, names)
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        return user_choice(matches)
