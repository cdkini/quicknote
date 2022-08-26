from typing import Tuple

import click

from qn.repo import Repo
from qn.shell import Shell
from qn.utils import determine_root


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system
    designed around speed and ease-of-use.
    """
    root = determine_root()
    shell = Shell(editor="nvim")
    repo = Repo(root=root, shell=shell)
    ctx.obj = repo


@cli.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
def add_cmd(repo: Repo, name: str) -> None:
    """
    add cmd
    """
    repo.add_note(name)


@cli.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_cmd(repo: Repo, names: Tuple[str]) -> None:
    """
    open cmd
    """
    repo.open_notes(names)


@cli.command("daily")
@click.pass_obj
def daily_cmd(repo: Repo) -> None:
    """
    daily cmd
    """
    repo.open_daily_note()


@cli.command("ls")
@click.pass_obj
def ls_cmd(repo: Repo) -> None:
    """
    ls cmd
    """
    notes = repo.list_notes()
    for note in notes:
        click.echo(note)


@cli.command("grep")
@click.pass_obj
def grep_cmd(repo: Repo) -> None:
    """
    grep cmd
    """
    pass


@cli.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_cmd(repo: Repo, names: Tuple[str]) -> None:
    """
    rm cmd
    """
    repo.delete_notes(names)


if __name__ == "__main__":
    cli()
