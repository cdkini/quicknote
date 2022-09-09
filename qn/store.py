import difflib
import pathlib
from typing import Dict, List, Optional, Tuple

from qn.shell import Shell
from qn.utils import user_choice, user_confirmation


class NoteStore:
    def __init__(self, root: pathlib.Path, shell: Shell) -> None:
        self._root = root
        self._shell = shell
        self._notes = self._init_notes()

    def _init_notes(self) -> Dict[str, pathlib.Path]:
        paths = list(
            filter(
                lambda n: n.is_file() and not n.stem.startswith("."),
                self._root.iterdir(),
            )
        )
        return {path.stem: path for path in paths}

    def add(self, name: str) -> None:
        if name in self._notes:
            raise FileExistsError(f"'{name}' already exists")

        path = self._determine_path_from_name(name)
        self._shell.open([path])

    def open(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        self._shell.open(paths)

    def list(self) -> List[str]:
        return sorted(self._notes.keys())

    def delete(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        for path in paths:
            confirmation = user_confirmation(f"Delete '{path.stem}' [y/n]: ")
            if confirmation:
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
        paths = list(self._notes.values())
        names = self._shell.fzf(self._root, paths)
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
        names = list(self._notes.keys())
        matches = difflib.get_close_matches(name, names)
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        return user_choice(matches)
