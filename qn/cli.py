from typing import Tuple

import click

from qn.repo import Repo


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system
    designed around speed and ease-of-use.
    """
    repo = Repo.create()
    ctx.obj = repo
    ctx.call_on_close(repo.log)


@cli.command("config")
@click.pass_obj
def config_cmd(repo: Repo) -> None:
    """
    WIP - Configure quicknote settings.
    """
    raise NotImplementedError()


@cli.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
def add_cmd(repo: Repo, name: str) -> None:
    """
    Create a new note.
    """
    repo.add(name)


@cli.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_cmd(repo: Repo, names: Tuple[str]) -> None:
    """
    Open an existing note.
    """
    repo.open(names)


@cli.command("put")
@click.pass_obj
@click.argument("name", nargs=1)
def put_cmd(repo: Repo, name: str) -> None:
    """
    Open a note if it exists else create a new one.
    """
    repo.put(name)


@cli.command("daily")
@click.pass_obj
def daily_cmd(repo: Repo) -> None:
    """
    Open your daily note (formatted YYYY-MM-DD).
    """
    repo.daily()


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
    Delete notes.
    """
    repo.delete(names)


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_obj
@click.argument("args", nargs=-1)
def grep_cmd(repo: Repo, args: Tuple[str, ...]) -> None:
    """
    Use ripgrep to search through notes.
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
    Get status of notes with git.
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
