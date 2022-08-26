import contextlib
import os
import pathlib
from typing import Generator


def determine_root() -> pathlib.Path:
    """

    Returns:

    """
    path = os.environ.get("QN_ROOT")
    if path is None:
        raise ValueError("No value found for QN_ROOT env var")

    root = pathlib.Path(path)
    if not root.exists():
        raise ValueError(f"QN_ROOT '{path}' does not exist")
    if not root.is_dir():
        raise ValueError(f"QN_ROOT '{path}' is not a directory")

    return root


# https://stackoverflow.com/a/13847807
@contextlib.contextmanager
def pushd(new_dir: str) -> Generator:
    """

    Args:
        new_dir (str):

    Returns:

    """
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)
