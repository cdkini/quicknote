from typing import List, Tuple

from qn.shell import Shell
from qn.store import NoteStore, TemplateStore
from qn.utils import determine_root


class Repo:
    def __init__(self, notes: NoteStore, templates: TemplateStore) -> None:
        self._notes = notes
        self._templates = templates

    @classmethod
    def create(cls) -> "Repo":
        root = determine_root()
        templates_root = root.joinpath(".templates")
        shell = Shell()

        notes = NoteStore(root=root, shell=shell)
        templates = TemplateStore(root=templates_root, shell=shell)

        return cls(notes=notes, templates=templates)

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

    def add_template(self, name: str) -> None:
        self._templates.add(name)

    def open_templates(self, names: Tuple[str, ...]) -> None:
        self._templates.open(names)

    def list_templates(self) -> List[str]:
        return self._templates.list()

    def delete_templates(self, names: Tuple[str, ...]) -> None:
        self._templates.delete(names)
