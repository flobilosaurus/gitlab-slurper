"""Module for exporting variables into local shell environment.
Works only with a shell wrapper function (see setup.py)
"""

import click
from pyslurp.variables.variable_container import VariableContainer


def has_boolean_value(variable) -> bool:
    """Check if the variable value is a boolean value."""
    return isinstance(variable.value, bool)


def _has_string_value(variable) -> bool:
    """Check if the variable value is a non-empty string value."""
    return variable.value and isinstance(variable.value, str)


@click.command("shell")
@click.option('--variable-export-file', default="vars",
              help="Path of the file which to export variables to.")
@click.pass_obj
def export(variables: VariableContainer, variable_export_file: str):
    """Saves export statements into a file
    which is interpreted by the wrapper function"""
    print(f"Exporting (file: {variable_export_file}) ...")
    with open(variable_export_file, "w", encoding='utf-8') as output:
        for variable in variables.get_vars():
            if has_boolean_value(variable):
                output.write(
                    f"export '{variable.key}'=\"{str(variable.value).lower()}\"\n")
            elif _has_string_value(variable) and '"' in variable.value and "'" in variable.value:
                click.echo(click.style(f"\nVariable {variable.key} value contains both, single and"
                                       " double quotes simultaneously. "
                                       "This is currently not supported. "
                                       "This variable will be skipped.\n", fg='red'))
            elif _has_string_value(variable) and "'" in variable.value:
                output.write(f"export '{variable.key}'=\"{variable.value}\"\n")
            else:
                output.write(f"export '{variable.key}'='{variable.value}'\n")
            print(f'{variable.key} ', end='')
    print("\n\nDone.")
