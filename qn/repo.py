from typing import List, Tuple

from qn.store import NoteStore


class Repo:
    def __init__(self, notes: NoteStore) -> None:
        self._note_store = notes

    def add_note(self, name: str) -> None:
        self._note_store.add(name)

    def open_notes(self, names: Tuple[str, ...]) -> None:
        self._note_store.open(names)

    def open_daily_note(self) -> None:
        self._note_store.open_daily()

    def list_notes(self) -> List[str]:
        return self._note_store.list()

    def delete_notes(self, names: Tuple[str, ...]) -> None:
        self._note_store.delete(names)

    def grep_notes(self, args: Tuple[str, ...]) -> None:
        self._note_store.grep(args)
