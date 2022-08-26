import datetime as dt
import pathlib
from typing import List, Tuple

from qn.shell import Shell


class Repo:
    def __init__(self, root: pathlib.Path, shell: Shell) -> None:
        self._root = root
        self._shell = shell

    def add_note(self, name: str) -> None:
        """

        Args:
            name (str):
        """
        path = self._determine_path_from_name(name)
        if path.exists():
            raise FileExistsError(f"Note '{name}' already exists; please use 'qn open'")

        self._shell.open([path])

    def open_notes(self, names: Tuple[str, ...]) -> None:
        """

        Args:
            names (Tuple[str, ...]):
        """
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._collect_paths_from_names(names)
        self._shell.open(paths)

    def open_daily_note(self) -> None:
        """ """
        today = str(dt.date.today())

        try:
            self.add_note(today)
        except FileExistsError:
            self.open_notes((today,))

    def list_notes(self) -> List[str]:
        """

        Returns:

        """
        notes = self._retrieve_all_note_paths()
        return sorted(map(lambda n: n.name, notes))

    def delete_notes(self, names: Tuple[str, ...]) -> None:
        """

        Args:
            names (Tuple[str, ...]):
        """
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._collect_paths_from_names(names)
        for path in paths:
            self._shell.user_confirmation(f"Delete '{path.stem}' [y/n]: ")
            path.unlink()

    def grep_through_notes(self, args: Tuple[str, ...]) -> None:
        self._shell.grep(self._root, args)

    def _interactively_retrieve_names(self) -> Tuple[str, ...]:
        notes = self._retrieve_all_note_paths()
        names = self._shell.fzf(self._root, notes)
        return names

    def _retrieve_all_note_paths(self) -> List[pathlib.Path]:
        return list(filter(lambda n: n.is_file(), self._root.iterdir()))

    def _collect_paths_from_names(self, names: Tuple[str, ...]) -> List[pathlib.Path]:
        paths = []
        for name in names:
            path = self._determine_path_from_name(name)
            if not path.exists():
                raise FileNotFoundError(f"Note '{name}' does not exist")
            paths.append(path)

        return paths

    def _determine_path_from_name(self, name: str) -> pathlib.Path:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        return path
