"""PySlurp system wide Constants"""

from pathlib import Path

SOURCES_CONFIG_KEY = "sources"
SLURPER_CONFIG_FILE_NAME = '.pyslurp.yaml'
GIT_CONFIG_FILE_NAME = '.git/config'
USER_DIR = str(Path.home())
GLOBAL_CONFIG_DIR = f"{USER_DIR}/.pyslurp"
GLOBAL_CONFIG_PATH = f"{GLOBAL_CONFIG_DIR}/config.yml"
DEFAULTS = "defaults"
OVERRIDES = "overrides"
INJECT_SCRIPT = "inject_script"
