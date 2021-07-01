import os
from pathlib import Path
import yaml

from exceptions import ConfigNotFoundException, ConfigInvalidException

CONFIG_FILE_NAME = '.pyslurp.yaml'
USER_DIR = str(Path.home())
GLOBAL_CONFIG_DIR = f"{USER_DIR}/.pyslurp"
GLOBAL_CONFIG_PATH = f"{GLOBAL_CONFIG_DIR}/config.yaml"

def get_path_to_local_config():
    """Helper: Retrieves path to the gslurp config file"""
    current_path = os.getcwd()
    while (True):
        if os.path.isfile(current_path + '/' + CONFIG_FILE_NAME):
            return current_path + '/' + CONFIG_FILE_NAME
        current_path = os.path.dirname(current_path)
        if current_path is '/':
            raise ConfigNotFoundException("Configuration file not found.")


def load_yaml(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def get_local_config():
    path = get_path_to_local_config()
    return load_yaml(path)


def get_global_config():
    path = GLOBAL_CONFIG_PATH
    return load_yaml(path)

def get_credentials(source, name):
    config = get_global_config()
    if config[source] is None:
        raise ConfigNotFoundException(f"No configs found for source type {source}.")
    sources = [source_config for source_config in config[source] if source_config["name"] == name]
    if len(sources) > 1:
        raise ConfigInvalidException(f"Global config is invalid: found multiple configs for '{name}' in {GLOBAL_CONFIG_PATH}.")
    if len(sources) < 1:
        raise ConfigNotFoundException(f"No config found for '{name}' in {GLOBAL_CONFIG_PATH}.")
    return sources[0]
