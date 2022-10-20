from __future__ import annotations

import json
import pathlib
from dataclasses import asdict, dataclass


@dataclass
class Config:
    def __init__(
        self,
        editor: str = "vim",  # Alternative - nvim
        grep_cmd: str = "grep",  # Alternative - rg or ag
        git_remote_name: str = "origin",
        # Alternative - '-m --preview "bat --style=numbers --color=always --line-range :500 {}"'
        fzf_opts: str = '-m --preview "cat {}"',
    ) -> None:
        self.editor = editor
        self.grep_cmd = grep_cmd
        self.git_remote_name = git_remote_name
        self.fzf_opts = fzf_opts

    @classmethod
    def parse_from_root(cls, root: pathlib.Path) -> Config:
        config_path = root.joinpath(".config")
        if not config_path.exists():
            config = cls()
            config.write_to_disk(config_path)
            return config

        with open(config_path) as f:
            data = json.load(f)
        return cls(**data)

    def write_to_disk(self, path: pathlib.Path) -> None:
        data = asdict(self)
        with path.open("w") as f:
            json.dump(data, f, indent=4)
