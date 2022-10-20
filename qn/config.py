from __future__ import annotations

import json
import pathlib
from dataclasses import asdict, dataclass


@dataclass
class Config:
    editor = "vim"  # Alternative - nvim
    grep_cmd = "grep"  # Alternative - rg or ag
    git_remote_name = "origin"
    # Alternative - '-m --preview "bat --style=numbers --color=always --line-range :500 {}"'
    fzf_opts = '-m --preview "cat {}"'

    # TODO(cdkini): Use a better config file format than JSON

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
        with path.open("w") as f:
            data = asdict(self)
            json.dump(data, f, indent=4)
