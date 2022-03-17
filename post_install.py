"""Creates global config and the shell wrapper"""

import os

from pathlib import Path

import jinja2
from jinja2 import FileSystemLoader

from configuration.config_manager import GLOBAL_CONFIG_PATH
from configuration.keys.gitlab_keys import GITLAB_URL_KEY, GITLAB_CONFIG_KEY, GITLAB_TOKEN_KEY
from configuration.keys.config_keys import SOURCES_CONFIG_KEY, GLOBAL_CONFIG_DIR, USER_DIR
from exceptions import UnsupportedShellException

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


def post_install():
    """Creates global config and shell wrapper"""
    create_global_config()
    create_shell_wrapper()


def create_global_config():
    """Creates .pyslurp directory in your home directory
    along with an empty global config"""
    configfile = Path(GLOBAL_CONFIG_PATH)
    if configfile.is_file():
        print(f"Configuration file already exists in {GLOBAL_CONFIG_PATH}")
        print("You have to delete it first.")
        return
    Path(GLOBAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    configfile.touch(exist_ok=True)
    template_name = "global_config.j2"
    template_path = f"{SCRIPT_DIR}/configuration/templates"
    shell_wrapper_template = load_template(template_path, template_name)
    global_config = shell_wrapper_template.render(
        sources_config_key=SOURCES_CONFIG_KEY,
        gitlab_config_key=GITLAB_CONFIG_KEY,
        gitlab_url_key=GITLAB_URL_KEY,
        gitlab_token_key=GITLAB_TOKEN_KEY
    )

    with open(configfile, "w") as output:
        output.write(global_config)
    print(f"Configuration created in {GLOBAL_CONFIG_PATH}")


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
    if wrapper_already_exists(function_name, shell_config_file):
        return
    hint = f"Please run:\nsource {shell_config_file}\n"
    "to register pyslurp in your system environment."
    add_wrapper_function_to_file(shell_config_file, wrapper_function, hint)

def _create_shell_wrapper_by_function_file(function_name, template_config):
    wrapper_function = render_wrapper_function(function_name, template_config)
    function_file_directory = template_config["function_file_directory"]
    function_file_suffix = template_config["function_file_suffix"]
    full_function_filename = f'{USER_DIR}/{function_file_directory}/{function_name}.{function_file_suffix}'
    if function_file_exists(full_function_filename):
        return
    add_wrapper_function_to_file(full_function_filename, wrapper_function)

def add_wrapper_function_to_file(filename, wrapper_function, hint=None):
    """Writes rendered wrapper function to the given file."""
    with open(filename, "a+") as f:
        f.write("\n")
        f.write(wrapper_function)
    print("Install successful.")
    if hint:
        print(hint)

def wrapper_already_exists(function_name, shell_config_file):
    """Checks if the wrapper function already exists."""
    with open(shell_config_file, "r") as config_file:
        data = config_file.read()
        if function_name in data:
            print(f"Function starting with signature {function_name} "
                  f"already exists in {shell_config_file}.")
            print(
                f"Please review your {shell_config_file} and remove this function.")
            return True
        return False

def function_file_exists(full_function_filename):
    file_exists = os.path.exists(full_function_filename)
    if file_exists:
            print(f"Function file {full_function_filename} already exists."
                  f"Please remove it first.")
            return True
    return False

def get_template_config():
    """Determines the current system shell and loads a corresponding template."""
    shell_type = os.getenv("SHELL").split("/")[-1]
    if shell_type not in supported_shells.keys():
        message = f"The shell f{shell_type} is not supported by pyslurp." \
                  f" Only the following shells are supported {', '.join(supported_shells.keys())}."
        raise UnsupportedShellException(message)
    template_config = supported_shells[shell_type]
    return template_config


def render_wrapper_function(function_name, template_config):
    """Substitutes variables in the Jinja2 template and generates the wrapper function."""
    script_ref = "_pyslurp"
    template_name = template_config["template_file"]
    template_path = f"{SCRIPT_DIR}/configuration/templates/shell_wrappers"
    shell_wrapper_template = load_template(template_path, template_name)
    wrapper_function = shell_wrapper_template.render(
        function_name=function_name,
        script_path=script_ref
    )
    return wrapper_function


def load_template(path, template_name):
    """Loads Jinja2 template from file."""
    template_loader = FileSystemLoader(path)
    template_env = jinja2.Environment(loader=template_loader)
    shell_wrapper_template = template_env.get_template(template_name)
    return shell_wrapper_template
