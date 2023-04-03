"""Loads variables from defaults and overrides block"""
import subprocess

from pyslurp.configuration.config_manager import get_global_config, get_local_config
from pyslurp.configuration.keys.config_keys import DEFAULTS, OVERRIDES, INJECT_SCRIPT
from pyslurp.variables.variable import Variable


def get_overrides():
    """Loads override values for variables."""
    global_overrides = _handle_global_config(OVERRIDES)
    local_overrides = _handle_local_config(OVERRIDES)
    return global_overrides, local_overrides


def get_defaults():
    """Loads default values for variables."""
    global_defaults = _handle_global_config(DEFAULTS)
    local_defaults = _handle_local_config(DEFAULTS)
    return global_defaults, local_defaults


def _handle_local_config(variable_type):
    local_config = get_local_config()
    return _handle_config(local_config, variable_type)


def _handle_global_config(variable_type):
    global_config = get_global_config()
    return _handle_config(global_config, variable_type)


def _handle_config(config, variable_type):
    variables = {}
    if variable_type in config:
        defaults_map = config[variable_type]
        for key in defaults_map.keys():
            variable = defaults_map[key]
            value = _evaluate_for_script(variable)
            variables[key] = Variable(key, value)
    return variables


def _evaluate_for_script(variable_value: str):
    """
    Will execute the script, if provided and use the output value as
    the value for the environment variable.
    # FIXME: Currently only commands with single line output are supported.
    """
    if str(variable_value).startswith(INJECT_SCRIPT):
        command = variable_value[len(INJECT_SCRIPT)+1:-1].split(" ")
        output = subprocess.run(command, stdout=subprocess.PIPE, check=True)\
            .stdout.decode('utf-8')\
            .rstrip("\n")
        return output
    return variable_value
