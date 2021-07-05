from pathlib import Path

SOURCES_CONFIG_KEY = "sources"
CONFIG_FILE_NAME = '.pyslurp.yaml'
USER_DIR = str(Path.home())
GLOBAL_CONFIG_DIR = f"{USER_DIR}/.pyslurp"
GLOBAL_CONFIG_PATH = f"{GLOBAL_CONFIG_DIR}/config.yaml"