"""Loads and saves local and global config files"""
import os
import yaml

from configuration.keys.global_config import CONFIG_FILE_NAME, GLOBAL_CONFIG_PATH
from exceptions import ConfigNotFoundException

def get_path_to_local_config():
    """Helper: Retrieves path to the pyslurp config file"""
    current_path = os.getcwd()
    while True:
        if os.path.isfile(current_path + '/' + CONFIG_FILE_NAME):
            return current_path + '/' + CONFIG_FILE_NAME
        current_path = os.path.dirname(current_path)
        if current_path == '/':
            raise ConfigNotFoundException("Configuration file not found.")


def load_yaml(path):
    """Load data from YAML file."""
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def get_local_config():
    """Loads local configuration file (.pyslurp.yaml)"""
    path = get_path_to_local_config()
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
