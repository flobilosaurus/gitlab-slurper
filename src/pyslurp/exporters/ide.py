"""Module for exporting variables in IDE format"""

import click
from pyslurp.variables.variable_container import VariableContainer


@click.command("ide")
@click.pass_obj
def export(variables: VariableContainer):
    """Generates a semicolon separated string."""
    for variable in variables.get_vars():
        print(variable.key + '=' + variable.value + ';', end='')
