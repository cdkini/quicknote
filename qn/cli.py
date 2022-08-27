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


@cli.group(name="add")
@click.pass_context
def add(ctx: click.Context):
    pass


@add.command("note")
@click.pass_obj
@click.argument("name", nargs=1)
def add_note(repo: Repo, name: str) -> None:
    repo.add_note(name)


@add.command("tmpl")
@click.pass_obj
@click.argument("name", nargs=1)
def add_tmpl(repo: Repo, name: str) -> None:
    raise NotImplementedError()


@cli.group(name="open")
@click.pass_context
def open(ctx: click.Context):
    pass


@open.command("note")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_note(repo: Repo, names: Tuple[str]) -> None:
    repo.open_notes(names)


@open.command("tmpl")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_tmpl(repo: Repo, names: Tuple[str]) -> None:
    raise NotImplementedError()


@cli.group("ls")
@click.pass_obj
def ls(ctx: click.Context) -> None:
    pass


@ls.command("note")
@click.pass_obj
def ls_note(repo: Repo) -> None:
    notes = repo.list_notes()
    for note in notes:
        click.echo(note)


@ls.command("tmpl")
@click.pass_obj
def ls_tmpl(repo: Repo) -> None:
    raise NotImplementedError()


@cli.group("rm")
@click.pass_obj
def rm(ctx: click.Context) -> None:
    pass


@rm.command("note")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_note(repo: Repo, names: Tuple[str]) -> None:
    repo.delete_notes(names)


@rm.command("tmpl")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_tmpl(repo: Repo, names: Tuple[str]) -> None:
    raise NotImplementedError()


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_obj
@click.argument("args", nargs=-1)
def grep_cmd(repo: Repo, args: Tuple[str, ...]) -> None:
    repo.grep_notes(args)


@cli.command("daily")
@click.pass_obj
def daily_note(repo: Repo) -> None:
    repo.open_daily_note()


if __name__ == "__main__":
    cli()
