"""Module loads GitLab variables from Projects and groups"""
import gitlab as gl
from configuration.config_manager import get_global_config, get_local_config
from configuration.keys.gitlab_keys import GITLAB_ENDPOINT_KEY,\
    GITLAB_URL_KEY, GITLAB_TOKEN_KEY, GITLAB_CONFIG_KEY, \
    PROJECT_PATH_KEY, PROJECT_ENV_KEY
from configuration.keys.config_keys import SOURCES_CONFIG_KEY
from exceptions import ConfigNotFoundException,\
    GitProjectNotFoundException,\
    ConfigInvalidException,\
    GitGroupNotFoundException
from variables.variable import Variable


def fetch_variables():
    """Retrieves variables from GitLab"""
    local_config = get_local_config()
    gl_config = _load_gitlab_config(local_config)
    url = gl_config[GITLAB_ENDPOINT_KEY][GITLAB_URL_KEY]
    token = gl_config[GITLAB_ENDPOINT_KEY][GITLAB_TOKEN_KEY]
    print(f"Connecting to {url}")
    gitlab_client = gl.Gitlab(url=url, private_token=token)
    group_vars = _load_group_vars(gl_config, gitlab_client)
    project_vars = _load_project_vars(gl_config, gitlab_client)
    return group_vars, project_vars


def _load_gitlab_config(local_config):
    """Load configuration for the GitLab server"""
    if GITLAB_CONFIG_KEY not in local_config:
        raise ConfigNotFoundException(
            "No configuration for GitLab found in config file.")
    gitlab_config = local_config[GITLAB_CONFIG_KEY]
    gitlab_host = gitlab_config[GITLAB_URL_KEY]
    endpoint = _get_endpoint(gitlab_host)
    gitlab_config[GITLAB_ENDPOINT_KEY] = endpoint
    return gitlab_config


def _get_endpoint(gitlab_host):
    """Get GitLab server endpoint"""
    global_config = get_global_config()
    source_configs = [config for config in global_config[SOURCES_CONFIG_KEY][GITLAB_CONFIG_KEY] if
                      config[GITLAB_URL_KEY] == gitlab_host]
    if len(source_configs) < 1:
        raise ConfigNotFoundException(
            f"Configuration for host {gitlab_host} not found.")
    if len(source_configs) > 1:
        raise ConfigInvalidException(
            f"Multiple configurations for host {gitlab_host} found.")
    endpoint = source_configs[0]
    return endpoint


def _load_project_vars(gitlab_config, gitlab_client):
    """Load project variables"""
    if PROJECT_PATH_KEY not in gitlab_config:
        raise ConfigInvalidException(
            "Nor project path is specified int the configuration file.")
    variables = {}
    wanted_project = gitlab_config[PROJECT_PATH_KEY]
    valid_project = _find_project(gitlab_client, wanted_project)
    print(f"Loading variables from {valid_project.path_with_namespace}")
    project_env = gitlab_config[PROJECT_ENV_KEY] if PROJECT_ENV_KEY in gitlab_config else '*'

    def has_correct_scope(project):
        return project.environment_scope in ['*', project_env]
    remote_variables = filter(
        has_correct_scope, valid_project.variables.list(all=True))
    for variable in remote_variables:
        variables[variable.key] = \
            Variable(variable.key, variable.value, {
                     PROJECT_ENV_KEY: project_env})
    return variables


def _find_project(gitlab_client, wanted_project):
    """Find GitLab project by full path"""
    project_name = wanted_project.split("/")[-1]
    found_projects = gitlab_client.projects.list(search=project_name, all=True)
    matching_projects = [project for project in found_projects
                         if project.path_with_namespace == wanted_project]
    if len(matching_projects) == 0:
        raise GitProjectNotFoundException(
            f"Project with path {wanted_project} could not be found.")
    return matching_projects[0]


def _get_group_names(project_path):
    """Extract groups from project path"""
    if "/" not in project_path:
        print("Project not attached to any groups.")
        return []
    path_elements = project_path.split("/")
    path_elements.pop()
    return path_elements


def _load_group_vars(gitlab_config, gitlab_client):
    """Load group variables"""
    wanted_groups = _get_group_names(gitlab_config[PROJECT_PATH_KEY])
    variables = {}
    path_elements = []
    for wanted_group in wanted_groups:
        path_elements.append(wanted_group)
        valid_group = _find_group(gitlab_client, path_elements, wanted_group)
        print(f"Loading variables from {valid_group.full_path}")
        for variable in valid_group.variables.list(all=True):
            variables[variable.key] = Variable(variable.key, variable.value)
    return variables


def _find_group(gitlab_client, path_elements, wanted_group):
    """Find GitLab group by full path"""
    current_path = "/".join(path_elements)
    found_groups = gitlab_client.groups.list(search=wanted_group, all=True)
    matching_groups = [
        group for group in found_groups if group.full_path == current_path]
    if len(matching_groups) == 0:
        raise GitGroupNotFoundException(
            f"Group with path {wanted_group} could not be found.")
    valid_group = matching_groups[0]
    return valid_group
