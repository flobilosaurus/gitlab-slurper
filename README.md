#PySlurp
##Motivation
The purpuse of this tool is to simplify local development for projecct, that you also store in GitLab.
Very often you have to deal with a great amount of environment variables which are required for the operations in
GitLab CI. 

This script will help you to maintain your GitLab repository as a single source of truth for your environment variables.
It will pull the GitLab variables from the specified repository and its groups and export them to your local environment.

##Installation
This script requires an initial installation, which is done from the project root directory. Because of the way processes
and their environments behave on Linux, a wrapper bash function must be added to your .bashrc file.

Run tbe following to trigger the installation.
```python3 configuration install```

Finish the installation by running ```source .bashrc``` in your local directory.

This operation will also generate a configuration file in ~/.pyslurp/config.yml

## Configuration
###Global configuration
The global configuration file stores the repository endpoints with the access credentials. It can be found 
in ```~/.pyslurp/config.yml``` an will look as follows:
```yaml
sources:
  gitlab:
    - name: MyServerAlias
      url: https://your.gitlab.server.net/
      token: YourGitLabToken
```

### Sample local config file
This configuration file must exist in every directory from which you want to call **pyslurp**
The name parameter must correspond with the name of a server in the global config. 
```yaml
gitlab:
  name: MyServerAlias  #"Name referring to the alias in ~/.pyslurp/config.yml"
  projects:
    - path: group1/group2/your-project-name
      environment: playground
    - path: another-project-name
  groups:
    - a-gitlab-group-name
```

##Usage
In order to export the variables to your local environment, execute
```pyslurp gitlab shell``` in your terminal.
If you need semicolon separated values for your IDE instead, execute ```pyslurp gitlab shell```. 