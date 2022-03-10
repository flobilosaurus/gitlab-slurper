"""Loads and saves local and global config files"""
import os
import yaml

from configuration.keys.config_keys import SLURPER_CONFIG_FILE_NAME, GLOBAL_CONFIG_PATH
from exceptions import ConfigNotFoundException


def find_config(config_name):
    """Returns path to a config with the given name. Searches backwards in the dir hierarchy."""
    current_path = os.getcwd()
    while True:
        if os.path.isfile(current_path + '/' + config_name):
            return current_path + '/' + config_name
        current_path = os.path.dirname(current_path)
        if current_path == '/':
            raise ConfigNotFoundException(
                f"Configuration '{config_name}' could not be found.")


def local_config_exists():
    """Check if local configuration file exists."""
    try:
        return len(find_config(SLURPER_CONFIG_FILE_NAME)) > 0
    except ConfigNotFoundException:
        return False


def load_yaml(path):
    """Load data from YAML file."""
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def get_local_config():
    """Loads local configuration file (.pyslurp.yaml)"""
    path = find_config(SLURPER_CONFIG_FILE_NAME)
    return load_yaml(path)


def get_global_config():
    """Loads global config from ~/.pyslurp"""
    path = GLOBAL_CONFIG_PATH
    return load_yaml(path)


def save_yaml(config, path):
    """Saves data to yaml"""
    with open(path, 'w') as file:
        return yaml.safe_dump(config, file)


def save_global_config(config):
    """Saves global config to ~/.pyslurp"""
    save_yaml(config, GLOBAL_CONFIG_PATH)
