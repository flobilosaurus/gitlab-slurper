"""CLI wrapper for GitLab modules"""

import click

from exporters import ide, shell
from sources.gitlab.gitlab_handler import fetch_variables
from variables.variable_container import VariableContainer


@click.group("gitlab")
@click.pass_obj
def gitlab(variables: VariableContainer):
    """Pull variables from GitLab"""
    group_vars, project_vars = fetch_variables()
    variables.add_source(group_vars)
    variables.add_source(project_vars)


# Exporter bindings
gitlab.add_command(ide.export)
gitlab.add_command(shell.export)
