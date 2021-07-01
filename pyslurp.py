"""Main pyslurp CLI wrapper"""
import click

import configuration.config_cli
import sources.gitlab.cli


@click.group()
def cli():
    """CLI to export remote variables to your local environment"""
    pass


cli.add_command(sources.gitlab.cli.gitlab)
cli.add_command(configuration.config_cli.configuration)

if __name__ == '__main__':
    cli()
