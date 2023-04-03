"""Module creates a shell wrapper for _pyslurp"""
import os
from pathlib import Path

import click

from pyslurp.configuration.config_manager import load_template
from pyslurp.configuration.keys.config_keys import USER_DIR
from pyslurp.exceptions import UnsupportedShellException

SCRIPT_DIR = str(Path(__file__).parent)


supported_shells = {
    "bash": {
        "template_file": "bash.j2",
        "shell_config_file": ".bashrc"
    },
    "zsh": {
        "template_file": "zsh.j2",
        "shell_config_file": ".zshrc"
    },
    "fish": {
        "template_file": "fish.j2",
        "function_file_directory": ".config/fish/functions",
        "function_file_suffix": "fish"
    }
}


@click.command("create-shell-wrapper")
def create_shell_wrapper():
    """Creates a shell wrapper for pyslurp"""
    function_name = "pyslurp"
    template_config = get_template_config()
    if 'shell_config_file' in template_config:
        _create_shell_wrapper_by_config_entry(function_name, template_config)
    else:
        _create_shell_wrapper_by_function_file(function_name, template_config)


def _create_shell_wrapper_by_config_entry(function_name, template_config):
    wrapper_function = render_wrapper_function(function_name, template_config)
    shell_config_file = f"{USER_DIR}/{template_config['shell_config_file']}"
    if _wrapper_already_exists(wrapper_function, shell_config_file):
        return
    _add_wrapper_function_to_file(shell_config_file, wrapper_function)


def _create_shell_wrapper_by_function_file(function_name, template_config):
    wrapper_function = render_wrapper_function(function_name, template_config)
    function_file_directory = template_config["function_file_directory"]
    function_file_suffix = template_config["function_file_suffix"]
    full_function_filename = f'{USER_DIR}/' \
                             f'{function_file_directory}/' \
                             f'{function_name}.' \
                             f'{function_file_suffix}'
    if _function_file_exists(full_function_filename):
        return
    _add_wrapper_function_to_file(full_function_filename, wrapper_function)


def _add_wrapper_function_to_file(filename, wrapper_function):
    """Writes rendered wrapper function to the given file."""
    print(f"Would add following lines to {filename}")
    print(wrapper_function)
    if click.confirm("Continue?"):
        with open(filename, "a+", encoding="utf-8") as file:
            file.write("\n")
            file.write(wrapper_function)
        print("Install successful.")
        return
    print("Wrapper creation aborted.")


def _wrapper_already_exists(wrapper_function, shell_config_file):
    """Checks if the wrapper function already exists."""
    with open(shell_config_file, "r", encoding="utf-8") as config_file:
        data = config_file.read()
        if wrapper_function in data:
            print(f"Wrapper function detected in {shell_config_file}")
            return True
        return False


def _function_file_exists(full_function_filename):
    file_exists = os.path.exists(full_function_filename)
    if file_exists:
        print(f"Wrapper function detected in {full_function_filename}")
        return True
    return False


def get_template_config():
    """Determines the current system shell and loads a corresponding template."""
    shell_type = os.getenv("SHELL").split("/")[-1]
    if shell_type not in supported_shells:
        message = f"The shell {shell_type} is not supported by pyslurp." \
                  f" Only the following shells are supported {', '.join(supported_shells.keys())}."
        raise UnsupportedShellException(message)
    template_config = supported_shells[shell_type]
    return template_config


def render_wrapper_function(function_name, template_config):
    """Substitutes variables in the Jinja2 template and generates the wrapper function."""
    script_ref = "_pyslurp"
    template_name = template_config["template_file"]
    template_path = f"{SCRIPT_DIR}/templates/shell_wrappers"
    shell_wrapper_template = load_template(template_path, template_name)
    wrapper_function = shell_wrapper_template.render(
        function_name=function_name,
        script_path=script_ref
    )
    return wrapper_function
