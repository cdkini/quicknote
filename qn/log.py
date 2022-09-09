import datetime as dt
import pathlib
from typing import List


class CommandLogger:
    def __init__(self, root: pathlib.Path) -> None:
        self._root = root

    def log(self, args: List[str]) -> None:
        time = dt.datetime.now().isoformat()
        command = " ".join(arg for arg in args)
        entry = f"{time} - {command}\n"

        path = self._root.joinpath(".history.log")

        with path.open("a") as f:
            f.write(entry)
