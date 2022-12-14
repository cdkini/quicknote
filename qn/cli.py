import sys
from typing import Any, Tuple

import click

from qn.repo import Repo


class QnCLI(click.Group):
    def invoke(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Wrap invoke in try/except to remove stack traces from bad user commands.
        """
        try:
            super().invoke(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


@click.group(name="qn", cls=QnCLI)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system
    designed around speed and ease-of-use.
    """
    repo = Repo.create()
    repo.chdir()  # Temporary change directory to qn root so all cmds can use relative paths
    ctx.obj = repo
    repo.log()


@cli.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
def add_cmd(repo: Repo, name: str) -> None:
    """
    Create a new note.
    """
    repo.add(name=name, exists_ok=False)


@cli.command("upsert")
@click.pass_obj
@click.argument("name", nargs=1)
def upsert_cmd(repo: Repo, name: str) -> None:
    """
    Update a note if it exists or create a new one.
    """
    repo.add(name=name, exists_ok=True)


@cli.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_cmd(repo: Repo, names: Tuple[str]) -> None:
    """
    Open note(s).
    """
    repo.open(names=names)


@cli.command("ls")
@click.option("-r", "--reverse", "reverse", is_flag=True, default=False)
@click.pass_obj
def ls_cmd(repo: Repo, reverse: bool) -> None:
    """
    List notes.
    """
    notes = repo.list(reverse=reverse)
    for note in notes:
        click.echo(note)


@cli.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_cmd(repo: Repo, names: Tuple[str]) -> None:
    """
    Delete note(s).
    """
    repo.delete(names)


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_obj
@click.argument("args", nargs=-1)
def grep_cmd(repo: Repo, args: Tuple[str, ...]) -> None:
    """
    Search through notes.
    """
    repo.grep(args)


@cli.command("sync")
@click.pass_obj
def sync_cmd(repo: Repo) -> None:
    """
    Sync notes with GitHub.
    """
    repo.sync()


@cli.command("status")
@click.pass_obj
def status_cmd(repo: Repo) -> None:
    """
    Get status of notes with Git.
    """
    repo.status()


@cli.command("web")
@click.pass_obj
def web_cmd(repo: Repo) -> None:
    """
    Open notes in GitHub.
    """
    repo.web()


if __name__ == "__main__":
    cli()
