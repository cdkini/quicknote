import contextlib
import os
from enum import Enum
from typing import Generator, List


class Sorter(str, Enum):
    NAME = "name"
    CREATED = "created"
    ACCESSED = "accessed"
    MODIFIED = "modified"


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
