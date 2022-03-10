"""Module for exporting variables into local shell environment.
Works only with a shell wrapper function (see setup.py)
"""

import click
from variables.variable_container import VariableContainer


@click.command("shell")
@click.pass_obj
def export(variables: VariableContainer):
    """Saves export statements into a file
    which is interpreted by the wrapper function"""
    print("Exporting...")
    with open("vars", "w") as output:
        for variable in variables.get_vars():
            output.write(f"export '{variable.key}'='{variable.value}'\n")
            print(f'{variable.key} ', end='')
    print("\n\nDone.")
