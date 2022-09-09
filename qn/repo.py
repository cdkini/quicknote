from typing import List, Tuple

from qn.shell import Shell
from qn.store import NoteStore
from qn.utils import determine_root


class Repo:
    def __init__(self, notes: NoteStore) -> None:
        self._notes = notes

    @classmethod
    def create(cls) -> "Repo":
        root = determine_root()
        shell = Shell()

        notes = NoteStore(root=root, shell=shell)
        return cls(notes=notes)

    def add_note(self, name: str) -> None:
        self._notes.add(name)

    def open_notes(self, names: Tuple[str, ...]) -> None:
        self._notes.open(names)

    def list_notes(self) -> List[str]:
        return self._notes.list()

    def delete_notes(self, names: Tuple[str, ...]) -> None:
        self._notes.delete(names)

    def open_daily_note(self) -> None:
        self._notes.open_daily()

    def grep_notes(self, args: Tuple[str, ...]) -> None:
        self._notes.grep(args)
