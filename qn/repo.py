from typing import List, Tuple

from qn.log import CommandLogger
from qn.shell import Shell
from qn.store import NoteStore
from qn.utils import determine_root


class Repo:
    def __init__(self, notes: NoteStore, logger: CommandLogger) -> None:
        self._notes = notes
        self._logger = logger

    @classmethod
    def create(cls) -> "Repo":
        root = determine_root()
        shell = Shell()

        notes = NoteStore(root=root, shell=shell)
        logger = CommandLogger(root=root)
        return cls(notes=notes, logger=logger)

    def add_note(self, name: str) -> None:
        self._notes.add(name)

    def open_notes(self, names: Tuple[str, ...]) -> None:
        self._notes.open(names)

    def list_notes(self) -> List[str]:
        return self._notes.list()

    def delete_notes(self, names: Tuple[str, ...]) -> None:
        self._notes.delete(names)

    def grep_notes(self, args: Tuple[str, ...]) -> None:
        self._notes.grep(args)

    def log_command(self) -> None:
        self._logger.log()

    def sync_notes(self) -> None:
        self._notes.sync()

    def status(self) -> None:
        self._notes.status()
