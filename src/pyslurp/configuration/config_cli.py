"""Configuration CLI wrapper"""
import click

from pyslurp.configuration import autoconfig, shell_wrapper


@click.group("configuration")
def configuration():
    """PySlurp configuration"""


configuration.add_command(autoconfig.autoconfig)
configuration.add_command(shell_wrapper.create_shell_wrapper)
