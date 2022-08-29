import datetime as dt
import pathlib
import shutil
from typing import List, Optional, Tuple

from qn.shell import Shell
from qn.template import TemplateEngine


class Store:
    def __init__(self, root: pathlib.Path, shell: Shell) -> None:
        self._root = root
        self._shell = shell

    def add(self, name: str, text: Optional[str] = None) -> None:
        path = self._determine_path_from_name(name)
        if path.exists():
            raise FileExistsError(f"'{name}' already exists")

        if text is not None:
            with path.open("w") as f:
                f.write(text)
                f.seek(0)

        self._shell.open([path])

    def open(self, names: Tuple[str, ...]) -> None:
        if len(names) == 0:
            names = self._interactively_retrieve_names()

        paths = self._determine_paths_from_names(names)
        self._shell.open(paths)

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

    def _interactively_retrieve_names(self) -> Tuple[str, ...]:
        paths = self._retrieve_paths_in_root()
        names = self._shell.fzf(self._root, paths)
        return names

    def _retrieve_paths_in_root(self) -> List[pathlib.Path]:
        return list(filter(lambda n: n.is_file(), self._root.iterdir()))

    def _determine_paths_from_names(self, names: Tuple[str, ...]) -> List[pathlib.Path]:
        paths = []
        for name in names:
            path = self._determine_path_from_name(name)
            if not path.exists():
                raise FileNotFoundError(f"'{name}' does not exist")
            paths.append(path)

        return paths

    def _determine_path_from_name(self, name: str) -> pathlib.Path:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        return path


class NoteStore(Store):
    def open_daily(self, text: str) -> None:
        today = str(dt.date.today())

        try:
            self.add(today, text)
        except FileExistsError:
            self.open((today,))


class TemplateStore(Store):
    def __init__(
        self, root: pathlib.Path, shell: Shell, engine: TemplateEngine
    ) -> None:
        super().__init__(root=root, shell=shell)
        self._engine = engine
        if not root.exists():
            self.scaffold()

    def scaffold(self) -> None:
        self._root.mkdir()
        self._create_daily_template()

    def evaluate_template(self, name: str) -> str:
        if not name.endswith(".md"):
            name += ".md"

        path = self._root.joinpath(name)
        if not path.exists():
            raise FileNotFoundError()

        with path.open() as f:
            contents = f.read()

        return self._engine.eval(contents)

    def _create_daily_template(self) -> None:
        src = pathlib.Path(__file__).joinpath("templates/daily.md")
        dst = self._root.joinpath("daily.md")
        assert src.exists()

        src_path = src.as_posix()
        dst_path = dst.as_posix()
        shutil.copy(src_path, dst_path)
