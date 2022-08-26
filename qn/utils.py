import os
import pathlib


def determine_root() -> pathlib.Path:
    path = os.environ.get("QN_ROOT")
    if path is None:
        raise ValueError("No value found for QN_ROOT env var")

    root = pathlib.Path(path)
    if not root.exists():
        raise ValueError(f"QN_ROOT '{path}' does not exist")
    if not root.is_dir():
        raise ValueError(f"QN_ROOT '{path}' is not a directory")

    return root