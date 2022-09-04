from typing import Optional, Tuple

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


@cli.group(name="note")
@click.pass_context
def note(ctx: click.Context):
    """
    Manage CRUD around notes.
    """
    pass


@note.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
@click.option("--template", "-t", default=None)
def add_note(repo: Repo, name: str, template: Optional[str]) -> None:
    """
    Create a new note.
    """
    repo.add_note(name, template)


@note.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_note(repo: Repo, names: Tuple[str]) -> None:
    """
    Open an existing note.
    """
    repo.open_notes(names)


@note.command("ls")
@click.pass_obj
def ls_note(repo: Repo) -> None:
    """
    List notes.
    """
    notes = repo.list_notes()
    for note in notes:
        click.echo(note)


@note.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_note(repo: Repo, names: Tuple[str]) -> None:
    """
    Delete notes.
    """
    repo.delete_notes(names)


@note.command("daily")
@click.pass_obj
def daily_note(repo: Repo) -> None:
    """
    Open daily note.
    """
    repo.open_daily_note()


@cli.group(name="tmpl")
@click.pass_context
def tmpl(ctx: click.Context):
    """
    Manage CRUD around templates.
    """
    pass


@tmpl.command("add")
@click.pass_obj
@click.argument("name", nargs=1)
def add_tmpl(repo: Repo, name: str) -> None:
    """
    Create a new temlate.
    """
    repo.add_template(name)


@tmpl.command("open")
@click.pass_obj
@click.argument("names", nargs=-1)
def open_tmpl(repo: Repo, names: Tuple[str]) -> None:
    """
    Open an existing template.
    """
    repo.open_templates(names)


@tmpl.command("ls")
@click.pass_obj
def ls_tmpl(repo: Repo) -> None:
    """
    List templates.
    """
    templates = repo.list_templates()
    for template in templates:
        click.echo(template)


@tmpl.command("rm")
@click.pass_obj
@click.argument("names", nargs=-1)
def rm_tmpl(repo: Repo, names: Tuple[str]) -> None:
    """
    Delete templates.
    """
    repo.delete_templates(names)


@cli.command(
    "grep", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.pass_obj
@click.argument("args", nargs=-1)
def grep_cmd(repo: Repo, args: Tuple[str, ...]) -> None:
    """
    Use ripgrep through parse through notes and templates.
    """
    repo.grep_notes(args)


if __name__ == "__main__":
    cli()
