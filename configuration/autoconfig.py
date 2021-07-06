"""Automatically creates .pyslurp.yml for GitLab from .git dir"""
import re
from pathlib import Path

import click
import gitlab
import jinja2
from gitlab import GitlabListError
from jinja2 import FileSystemLoader

from configuration.config_manager import get_global_config, save_global_config
from configuration.keys.gitlab import GITLAB_URL_KEY, GITLAB_TOKEN_KEY,\
    GITLAB_CONFIG_KEY, PROJECT_PATH_KEY, \
    PROJECT_ENV_KEY
from configuration.keys.global_config import SOURCES_CONFIG_KEY, CONFIG_FILE_NAME
from exceptions import ConfigInvalidException, ApiCheckFailedException


def add_auth_info(global_config, secure_host):
    """Adds auth data for Git server to global config"""
    token = click.prompt(
        f"Please enter a valid GitLab token for host {secure_host}.")
    host_config = {
        GITLAB_URL_KEY: secure_host,
        GITLAB_TOKEN_KEY: token
    }
    gitlab_client = gitlab.Gitlab(url=secure_host, private_token=token)
    try:
        gitlab_client.projects.list(page=1, per_page=1)
    except GitlabListError as error:
        raise ApiCheckFailedException(f"Error while making a test call to {secure_host}."
                                      " Check if server has a valid GitLab REST API.") from error
    global_config[SOURCES_CONFIG_KEY][GITLAB_CONFIG_KEY].append(host_config)


@click.command("autoconfig")
def autoconfig():
    """Generates .pyslurp.yaml from .git directory.
    Must be executed at a GitLab project root
    """
    secure_host = generate_local_config()
    add_entry_to_global_config(secure_host)


def generate_local_config():
    """Generates .pyslurp.yaml from Jinja2 template."""
    script_path = Path(__file__).parent
    template_loader = FileSystemLoader(f"{script_path}/templates")
    template_env = jinja2.Environment(loader=template_loader)
    local_config_template = template_env.get_template(".pyslurp.j2")
    with open('.git/config', 'r') as file:
        data = file.read().replace('\n', '')
        pattern = ".*(url = git@)(.*:.*)(.*\\.git)"
        git_config_uri = re.match(pattern, data)
        git_uri = git_config_uri[2]
        git_uri_components = git_uri.split(":")
        host = git_uri_components[0]
        secure_host = f"https://{host}/"
        path = git_uri_components[1]
        local_config = local_config_template.render(
            gitlab_key=GITLAB_CONFIG_KEY,
            gitlab_url_key=GITLAB_URL_KEY,
            gitlab_project_path_key=PROJECT_PATH_KEY,
            gitlab_environment_key=PROJECT_ENV_KEY,
            gitlab_url=secure_host,
            gitlab_project_path=path,
            gitlab_environment="\'*\'"
        )
        with open(CONFIG_FILE_NAME, "w") as local_config_file:
            local_config_file.write(local_config)
    return secure_host


def add_entry_to_global_config(secure_host):
    """Adds auth entry to global config."""
    global_config = get_global_config()
    source_configs = [config for config
                      in global_config[SOURCES_CONFIG_KEY][GITLAB_CONFIG_KEY]
                      if config[GITLAB_URL_KEY] == secure_host]
    if len(source_configs) == 1:
        print(f"Host {secure_host} configured in the global configuration.")
    if len(source_configs) > 1:
        raise ConfigInvalidException(
            f"Multiple configurations for host {secure_host} found.")
    if len(source_configs) < 1:
        add_auth_info(global_config, secure_host)
    save_global_config(global_config)