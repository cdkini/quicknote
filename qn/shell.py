import datetime as dt
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import List, Tuple


def git_add() -> None:
    subprocess.call(["git", "add", "."])


def git_commit() -> None:
    subprocess.call(["git", "commit", "-m", dt.datetime.now().isoformat()])


def git_push() -> None:
    subprocess.call(["git", "push"])


def git_status() -> None:
    subprocess.call(["git", "status"])


def git_get_remote_url(remote_name: str) -> str:
    out = subprocess.check_output(["git", "remote", "get-url", remote_name])
    return out.decode("utf-8").strip()


def open_with_editor(paths: List[pathlib.Path], editor: str) -> None:
    command = [editor]
    for path in paths:
        str_path = path.as_posix()
        command.append(str_path)
    subprocess.call(command)


def grep(args: Tuple[str, ...], grep_cmd: str) -> None:
    command = [grep_cmd]
    for arg in args:
        command.append(arg)
    subprocess.call(command)


def fzf(paths: List[pathlib.Path], fzf_opts: str) -> Tuple[str, ...]:
    choices = sorted(map(lambda p: p.name, paths))
    results = _fzf_prompt(choices=choices, fzf_options=fzf_opts)
    return tuple(results)


# Refactored from pyfzf: https://github.com/nk412/pyfzf/blob/master/pyfzf/pyfzf.py
def _fzf_prompt(choices: List[str], fzf_options: str = "") -> List[str]:
    if not shutil.which("fzf"):
        raise SystemError("Cannot find 'fzf' installed on PATH.")

    # Convert lists to strings [ 1, 2, 3 ] => "1\n2\n3"
    choices_str = "\n".join(map(str, choices))

    with tempfile.NamedTemporaryFile(delete=False) as input_file:
        with tempfile.NamedTemporaryFile(delete=False) as output_file:
            # Create an temp file with list entries as lines
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()

    # Invoke fzf externally and write to output file
    os.system(f'fzf {fzf_options} < "{input_file.name}" > "{output_file.name}"')

    # Get selected options
    selection = []
    with open(output_file.name, encoding="utf-8") as f:
        for line in f:
            selection.append(line.strip("\n"))

    os.unlink(input_file.name)
    os.unlink(output_file.name)

    return selection
