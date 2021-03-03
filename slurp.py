import json
import gitlab
import helper
from constants import *
import exporters

def slurp_variables(config):
    exporter = exporters.available_exporters[config[variable_exporter]]
    
    gl = gitlab.Gitlab(config[gitlab_base_url], private_token=config[gitlab_token])
    project = gl.projects.get(config[project_id])

    # respect variable hierarchie by first exporting group variables top down
    if(config[include_parent_groups]):
        for group_id in helper.get_parent_group_ids(gl, project):
            for group_variable in gl.groups.get(group_id).variables.list():
                exporter(group_variable)

    # then export (scoped) project variables
    variables_with_selected_scope = helper.build_filter_for_scoped_variables(config)
    for project_variable in filter(variables_with_selected_scope, project.variables.list()):
        exporter(project_variable)


if __name__ == '__main__':
    if(helper.should_init()):
        helper.write_initial_config()
    else:
        config = helper.get_config()
        slurp_variables(config)
