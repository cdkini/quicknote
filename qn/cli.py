import click


@click.group(name="qn")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    qn (quicknote) is a terminal-based notetaking system designed around speed and ease-of-use.
    """


if __name__ == "__main__":
    cli()
