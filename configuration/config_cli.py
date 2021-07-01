import click

from configuration import config_installer


@click.group("configuration")
def configuration():
    pass

configuration.add_command(config_installer.install)