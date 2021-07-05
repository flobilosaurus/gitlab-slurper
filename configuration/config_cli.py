import click

from configuration import autoconfig


@click.group("configuration")
def configuration():
    pass

configuration.add_command(autoconfig.autoconfig)