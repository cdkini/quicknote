import contextlib
import os
import pathlib
from enum import Enum
from typing import Generator, List


class Sorter(str, Enum):
    NAME = "name"
    CREATED = "created"
    ACCESSED = "accessed"
    MODIFIED = "modified"


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


# https://stackoverflow.com/a/13847807
@contextlib.contextmanager
def pushd(new_dir: str) -> Generator:
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def user_confirmation(prompt: str) -> bool:
    answer = input(prompt)
    return answer.lower() in ("y", "yes")


def user_choice(choices: List[str]) -> str:
    for i, choice in enumerate(choices):
        print(f"{i+1}: {choice}")

    selection = int(input("Choice: "))

    return choices[selection - 1]
