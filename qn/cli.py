import click

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
    repo = Repo(root=root)
    ctx.obj = repo


@cli.command("add")
@click.pass_obj
def add_cmd(repo: Repo) -> None:
    pass


@cli.command("open")
@click.pass_obj
def open_cmd(repo: Repo) -> None:
    pass


@cli.command("grep")
@click.pass_obj
def grep_cmd(repo: Repo) -> None:
    pass


@cli.command("rm")
@click.pass_obj
def rm_cmd(repo: Repo) -> None:
    pass


if __name__ == "__main__":
    cli()
