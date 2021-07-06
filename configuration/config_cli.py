"""Configuration CLI wrapper"""
import click

from configuration import autoconfig


@click.group("configuration")
def configuration():
    """PySlurp configuration"""


configuration.add_command(autoconfig.autoconfig)
