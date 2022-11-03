from __future__ import annotations

import json
import pathlib
from dataclasses import asdict, dataclass


@dataclass
class Config:

    FILE_PATH = ".config.json"

    def __init__(
        self,
        root: pathlib.Path,
        editor: str = "vim",
        grep_cmd: str = "grep",
        git_remote_name: str = "origin",
        fzf_opts: str = '-m --preview "cat {}"',
    ) -> None:
        self.root = root
        self.editor = editor
        self.grep_cmd = grep_cmd
        self.git_remote_name = git_remote_name
        self.fzf_opts = fzf_opts

    @classmethod
    def parse_from_root(cls, root: pathlib.Path) -> Config:
        config_path = root.joinpath(cls.FILE_PATH)
        if not config_path.exists():
            config = cls(root=root)
            config.write_to_disk(config_path)
            return config

        with open(config_path) as f:
            data = json.load(f)
        return cls(root=root, **data)

    def write_to_disk(self, path: pathlib.Path) -> None:
        data = asdict(self)
        with path.open("w") as f:
            json.dump(data, f, indent=4)
