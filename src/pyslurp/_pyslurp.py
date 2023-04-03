"""Main pyslurp CLI wrapper"""
import click

import pyslurp.configuration.config_cli
import pyslurp.sources.gitlab.cli
from pyslurp.configuration.config_manager import local_config_exists
from pyslurp.sources.config.config_handler import get_defaults, get_overrides
from pyslurp.variables.variable_container import VariableContainer


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """CLI to export remote variables to your local environment"""
    if local_config_exists():
        variables = _load_variables_from_config()
        ctx.obj = variables


def _load_variables_from_config():
    variables = VariableContainer()
    global_defaults, local_defaults = get_defaults()
    global_overrides, local_overrides = get_overrides()
    variables.add_overrides(global_overrides)
    variables.add_overrides(local_overrides)
    variables.add_defaults(global_defaults)
    variables.add_defaults(local_defaults)
    return variables


cli.add_command(pyslurp.sources.gitlab.cli.gitlab)
cli.add_command(pyslurp.configuration.config_cli.configuration)

if __name__ == '__main__':
    # pylint: disable=E1120
    cli()
