import click


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system designed around speed and ease-of-use.
    """


@cli.command("add")
@click.pass_obj
def add_cmd() -> None:
    pass


@cli.command("open")
@click.pass_obj
def open_cmd() -> None:
    pass


@cli.command("grep")
@click.pass_obj
def grep_cmd() -> None:
    pass


@cli.command("ls")
@click.pass_obj
def ls_cmd() -> None:
    pass


@cli.command("rm")
@click.pass_obj
def rm_cmd() -> None:
    pass


if __name__ == "__main__":
    cli()
