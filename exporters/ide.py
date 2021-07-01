from typing import List

import click
from variable import Variable


@click.command("ide")
@click.pass_obj
def export(variables: List[Variable]):
    """Generates a semicolon separated string."""
    for variable in variables:
        print(variable.key+ '=' +variable.value + ';', end='')
