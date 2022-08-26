from typing import Tuple

import click

from qn.editor import Editor
from qn.repo import Repo
from qn.utils import determine_root


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system
    designed around speed and ease-of-use.
    """
    root = determine_root()
    editor = Editor("nvim")
    repo = Repo(root=root, editor=editor)
    ctx.obj = repo


@cli.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
def add_cmd(repo: Repo, name: str) -> None:
    repo.add_note(name)


@cli.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_cmd(repo: Repo, names: Tuple[str]) -> None:
    repo.open_notes(names)


@cli.command("ls")
@click.pass_obj
def ls_cmd(repo: Repo) -> None:
    notes = repo.list_notes()
    for note in notes:
        click.echo(note)


@cli.command("grep")
@click.pass_obj
def grep_cmd(repo: Repo) -> None:
    pass


@cli.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_cmd(repo: Repo, names: Tuple[str]) -> None:
    repo.delete_notes(names)


if __name__ == "__main__":
    cli()
