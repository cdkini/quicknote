import datetime as dt
import difflib
import pathlib
from typing import List, Optional, Tuple

from qn.shell import Shell


class NoteStore:
    def __init__(self, root: pathlib.Path, shell: Shell) -> None:
        self._root = root
        self._shell = shell

    def add(self, name: str) -> None:
        path = self._determine_path_from_name(name)
        if path.exists():
            raise FileExistsError(f"'{name}' already exists")

        self._shell.open([path])

    def open(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        self._shell.open(paths)

    def open_daily(self) -> None:
        today = str(dt.date.today())

        try:
            self.add(today)
        except FileExistsError:
            self.open((today,))

    def open_last_edited(self) -> None:
        paths = self._retrieve_paths_in_root()
        last_edited = max(paths, key=lambda p: p.stat().st_mtime)
        name = last_edited.stem
        self.open((name,))

    def list(self) -> List[str]:
        paths = self._retrieve_paths_in_root()
        return sorted(map(lambda p: p.name, paths))

    def delete(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        for path in paths:
            self._shell.user_confirmation(f"Delete '{path.stem}' [y/n]: ")
            path.unlink()

    def grep(self, args: Tuple[str, ...]) -> None:
        self._shell.grep(self._root, args)

    def sync(self) -> None:
        self._shell.git_add(self._root)
        self._shell.git_commit(self._root)
        self._shell.git_push(self._root)

    def status(self) -> None:
        self._shell.git_status(self._root)

    def _interactively_retrieve_names(self) -> Tuple[str, ...]:
        paths = self._retrieve_paths_in_root()
        names = self._shell.fzf(self._root, paths)
        return names

    def _retrieve_paths_in_root(self) -> List[pathlib.Path]:
        return list(
            filter(
                lambda n: n.is_file() and not n.stem.startswith("."),
                self._root.iterdir(),
            )
        )

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
        paths = self._retrieve_paths_in_root()
        names = sorted(map(lambda p: p.stem, paths))
        matches = difflib.get_close_matches(name, names)
        if not matches:
            return None
        return matches[0]
