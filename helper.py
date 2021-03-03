import json
import sys
import os
from constants import *

# config helper
def should_init(): 
    return len(sys.argv) == 2 and sys.argv[1] == INIT_COMMAND

def write_initial_config(): 
    with open(CONFIG_FILE_NAME, 'w') as file:
        file.write(json.dumps(INITIAL_CONFIG, sort_keys=True, indent=4))

def get_config():
    with open(get_path_to_config()) as config_file:
            return json.load(config_file)

def get_path_to_config():
    external_config_given = len(sys.argv) > 1
    if(external_config_given):
        return sys.argv[1]
    else:
        if(has_local_config()):
            return CONFIG_FILE_NAME
        else:
            script_path = os.path.dirname(os.path.realpath(__file__))
            return script_path + '/' + CONFIG_FILE_NAME

def has_local_config(): 
    local_files = os.listdir('.')
    return CONFIG_FILE_NAME in local_files

# gitlab helper
def _get_parent_group_ids(gl, group_id):
    if(not group_id):
        return []
    group = gl.groups.get(group_id)
    return _get_parent_group_ids(gl, group.parent_id) + [group.id]

def get_parent_group_ids(gl, gitlab_project):
    parent_id = gitlab_project.namespace['id']
    return _get_parent_group_ids(gl, parent_id)

def build_filter_for_scoped_variables(config):
    selected_scopes = [all_environments_scopes]
    
    environment_scope = config[variable_environment_scope]
    if(environment_scope):
        selected_scopes.append(environment_scope)

    return lambda variable: variable.environment_scope in selected_scopes