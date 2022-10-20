import datetime as dt
import pathlib
import sys


class CommandLogger:

    FILE_NAME = ".history"

    def __init__(self, root: pathlib.Path) -> None:
        self._root = root

    def log(self) -> None:
        args = sys.argv[1:]
        time = dt.datetime.now().isoformat()

        for i, arg in enumerate(args):
            if len(arg.split(" ")) > 1:
                args[i] = f'"{arg}"'

        command = " ".join(arg for arg in args)
        entry = f"{time} - {command}\n"

        path = self._root.joinpath(self.FILE_NAME)

        with path.open("a") as f:
            f.write(entry)
