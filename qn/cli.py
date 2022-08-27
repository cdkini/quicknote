from typing import Tuple

import click

from qn.repo import Repo
from qn.shell import Shell
from qn.store import NoteStore
from qn.utils import determine_root


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system
    designed around speed and ease-of-use.
    """
    root = determine_root()
    shell = Shell()
    notes = NoteStore(root=root, shell=shell)
    repo = Repo(notes=notes)
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


@cli.command("daily")
@click.pass_obj
def daily_cmd(repo: Repo) -> None:
    repo.open_daily_note()


@cli.command("ls")
@click.pass_obj
def ls_cmd(repo: Repo) -> None:
    notes = repo.list_notes()
    for note in notes:
        click.echo(note)


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_obj
@click.argument("args", nargs=-1)
def grep_cmd(repo: Repo, args: Tuple[str, ...]) -> None:
    repo.grep_notes(args)


@cli.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_cmd(repo: Repo, names: Tuple[str]) -> None:
    repo.delete_notes(names)


if __name__ == "__main__":
    cli()
