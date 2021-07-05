import os
import yaml

from configuration.keys.global_config import CONFIG_FILE_NAME, GLOBAL_CONFIG_PATH
from exceptions import ConfigNotFoundException, ConfigInvalidException

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


def save_yaml(config, path):
    with open(path, 'w') as file:
        return yaml.safe_dump(config, file)


def save_global_config(config):
    save_yaml(config, GLOBAL_CONFIG_PATH)

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
