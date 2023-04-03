"""Module for exporting variables in .env format"""

import click
from pyslurp.variables.variable_container import VariableContainer


def _has_string_value(variable) -> bool:
    return variable.value and isinstance(variable.value, str)


@click.command("dotenv")
@click.pass_obj
def export(variables: VariableContainer):
    """Generates a .env formated string (e.g. key=value\nkey2=value2)."""
    print("Exporting...")
    with open(".env", "w", encoding="utf-8") as output:
        for variable in variables.get_vars():
            replaced_value = variable.value
            if _has_string_value(variable):
                replaced_value = variable.value.replace("\n", "\\n")
            output.write(f'{variable.key}={replaced_value}\n')
            print(f'{variable.key} ', end='')
    print("\n\nDone.")
