# exporter constants
exporter_environment_variable = 'environment_variable'
exporter_terraform_tfvars_format = 'terraform_tfvars_format'
exporter_node_dotenv_format = 'node_dotenv_format'

# config
gitlab_base_url = 'gitlab_base_url'
gitlab_token = 'gitlab_token'
variable_environment_scope = 'variable_environment_scope'
project_id = 'project_id'
include_parent_groups = 'include_parent_groups'
variable_exporter = 'variable_exporter'

INITIAL_CONFIG = {
    gitlab_base_url: '',
    gitlab_token: '',
    variable_environment_scope: '',
    project_id: '',
    include_parent_groups : False,
    variable_exporter: exporter_environment_variable
}

CONFIG_FILE_NAME = 'slurp.config.json'

# commands
INIT_COMMAND = 'init'

# environment scopes
all_environments_scopes = '*'