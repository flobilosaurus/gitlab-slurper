import click

from exporters import ide, shell
from sources.gitlab.gitlab import fetch_variables


@click.group("gitlab")
@click.pass_context
def gitlab(ctx: click.Context):
    variables = fetch_variables()
    ctx.obj = variables

# Exporter bindings
gitlab.add_command(ide.export)
gitlab.add_command(shell.export)