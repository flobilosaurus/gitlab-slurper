import constants

def to_environment_variable(variable):
    print('export '+variable.key+ '="' +variable.value + '"')

def to_terraform_tfvars_format(variable):
    # filter for terraform variables
    if (variable.key.startswith('TF_VAR_')):
        # multiline strings, see https://www.terraform.io/docs/configuration-0-11/variables.html#strings
        if '\n' in variable.value: 
            print(variable.key[7:]+ '=<<EOF\n' +variable.value +'\nEOF')
        else:
            print(variable.key[7:]+ '="' +variable.value +'"')

def to_node_dotenv_format(variable):
    if '\n' in variable.value: 
        print(variable.key + '="' +variable.value +'"')
    else:
        print(variable.key + '=' +variable.value)

available_exporters = {
    constants.exporter_environment_variable: to_environment_variable,
    constants.exporter_terraform_tfvars_format: to_terraform_tfvars_format,
    constants.exporter_node_dotenv_format: to_node_dotenv_format
}