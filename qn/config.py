from __future__ import annotations

import pathlib
from dataclasses import dataclass

import toml


@dataclass
class Config:

    FILE_PATH = ".config.toml"

    def __init__(
        self,
        editor: str = "vim",
        grep_cmd: str = "grep",
        git_remote_name: str = "origin",
        fzf_opts: str = '-m --preview "cat {}"',
    ) -> None:
        self.editor = editor
        self.grep_cmd = grep_cmd
        self.git_remote_name = git_remote_name
        self.fzf_opts = fzf_opts

    @classmethod
    def parse_from_root(cls, root: pathlib.Path) -> Config:
        config_path = root.joinpath(cls.FILE_PATH)
        if not config_path.exists():
            config = cls()
            config.write_to_disk(config_path)
            return config

        with open(config_path) as f:
            data = toml.load(f)
        return cls(**data)

    def write_to_disk(self, path: pathlib.Path) -> None:
        data = self.__dict__
        with path.open("w") as f:
            toml.dump(data, f)
