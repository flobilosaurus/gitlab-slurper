from pathlib import Path

import click

from configuration.config_loader import GLOBAL_CONFIG_PATH, GLOBAL_CONFIG_DIR, USER_DIR


@click.command("install")
def install():
    create_global_config()
    create_shell_wrapper()

def create_global_config():
    configfile = Path(GLOBAL_CONFIG_PATH)
    if configfile.is_file():
        print(f"Configuration file already exists in {GLOBAL_CONFIG_PATH}")
        print("You have to delete it first.")
        return
    Path(GLOBAL_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    configfile.touch(exist_ok=True)
    template = """
# CONFIGURATION REFERENCE:
#
# sources:
#   gitlab:
#     - name: MyGitServerAlias
#       url: https://my.git.domain.net
#       token: YourGitLabToken
"""
    with open(configfile, "w") as output:
        output.write(template)
    print(f"Configuration created in {GLOBAL_CONFIG_PATH}")


def create_shell_wrapper():
    script_dir = str(Path(__file__).parent)
    script_path = '/'.join(script_dir.split("/")[:-1]) + "/pyslurp.py"
    function_signatuire = "pyslurp () {"

    wrapper_function = f"""
{function_signatuire}""" + f"""
    python3 {script_path} $*
    if [[ -f vars ]]; then
        source vars && rm vars
    fi
""" + """}"""
    bashrc_path = f"{USER_DIR}/.bashrc"
    with open(bashrc_path, "r") as bashrc:
        data = bashrc.read()
        if function_signatuire in data:
            print(f"Function starting with signature {function_signatuire} already exists in {bashrc_path}.")
            print(f"Please review your {bashrc_path} and remove this function.")
            return
    with open(bashrc_path, "a+") as bashrc:
        bashrc.write(wrapper_function)
    print("Install successfull.")
    print(f"Please run 'source {bashrc_path}' to register pyslurp in your system environment.")


