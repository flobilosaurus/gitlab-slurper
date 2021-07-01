import gitlab
from configuration.config_loader import get_global_config, get_local_config
from exceptions import ConfigNotFoundException, ProjectNotFoundException, ConfigInvalidException
from variable import Variable

def fetch_variables():
    """Retrieves variables from GitLab"""
    local_config = get_local_config()
    gitlab_config = load_gitlab_config(local_config)
    gitlab_client = gitlab.Gitlab(url=gitlab_config["endpoint"]["url"], private_token=gitlab_config["endpoint"]["token"])
    group_vars = load_group_vars(gitlab_config, gitlab_client)
    project_vars = load_project_vars(gitlab_config, gitlab_client)
    for key in group_vars.keys():
        if key in project_vars.keys():
            group_vars.pop(key)
    return list(group_vars.values()) + list(project_vars.values())


def load_gitlab_config(local_config):
    if "gitlab" not in local_config:
        raise ConfigNotFoundException("No configuration for GitLab found in config file.")
    gitlab_config = local_config["gitlab"]
    server_name = gitlab_config["name"]
    endpoint = get_endpoint(server_name)
    gitlab_config["endpoint"] = endpoint
    return gitlab_config


def get_endpoint(server_name):
    global_config = get_global_config()
    source_configs = [config for config in global_config["sources"]["gitlab"] if config["name"] == server_name]
    if len(source_configs) < 1:
        raise ConfigNotFoundException(f"Configuration for name {server_name} not found.")
    if len(source_configs) > 1:
        raise ConfigInvalidException(f"Multiple configurations for name {server_name} found.")
    endpoint = source_configs[0]
    return endpoint


def load_project_vars(gitlab_config, gitlab_client):
    if "projects" not in gitlab_config:
        return {}
    variables = {}
    valid_projects = []
    project_envs = {}
    for wanted_project in gitlab_config["projects"]:
        project_name = wanted_project["path"].split("/")[-1]
        found_projects = gitlab_client.projects.list(search=project_name, all=True)
        matching_projects = [project for project in found_projects if project.path_with_namespace == wanted_project["path"]]
        if len(matching_projects) == 0:
            raise ProjectNotFoundException(f"Project with path {wanted_project['path']} could not be found.")
        valid_projects.append(matching_projects[0])
        project_envs[wanted_project["path"]] = wanted_project["environment"] if 'environment' in wanted_project else '*'
    for wanted_project in valid_projects:
        custom_environment = project_envs[wanted_project.path_with_namespace]
        has_correct_scope = lambda project_config: project_config.environment_scope in ['*', custom_environment]
        print(f"Loading variables from {wanted_project.path_with_namespace}")
        remote_variables = filter(has_correct_scope, wanted_project.variables.list(all=True))
        for variable in remote_variables:
            variables[variable.key] = Variable(variable.key, variable.value, {'environment': custom_environment})
    return variables


def load_group_vars(gitlab_config, gitlab_client):
    if "groups" not in gitlab_config:
        return {}
    variables = {}
    valid_groups = []
    wanted_groups = list(sorted(gitlab_config["groups"], key = len))
    for wanted_group in wanted_groups:
        group_name = wanted_group.split("/")[-1]
        found_groups = gitlab_client.groups.list(search=group_name, all=True)
        matching_groups = [group for group in found_groups if group.full_path == wanted_group]
        if len(matching_groups) == 0:
            raise ProjectNotFoundException(f"Project with path {wanted_group} could not be found.")
        valid_groups.append(matching_groups[0])
    for group in valid_groups:
        print(f"Loading variables from {group.full_path}")
        for variable in group.variables.list(all=True):
            variables[variable.key] = Variable(variable.key, variable.value)
    return variables

