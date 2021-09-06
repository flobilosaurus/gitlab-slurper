"""Module for exporting variables into local shell environment.
Works only with a shell wrapper function (see setup.py)
"""
from typing import List

import click
from variable import Variable


@click.command("shell")
@click.pass_obj
def export(variables: List[Variable]):
    """Saves export statements into a file
    which is interpreted by the wrapper function"""
    print("Exporting...")
    with open("vars", "w") as output:
        for variable in variables:
            output.write(f'export {variable.key}="{variable.value}"\n')
            print(f'{variable.key} ', end='')
    print("\n\nDone.")
