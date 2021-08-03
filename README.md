#PySlurp

##Motivation
The purpuse of this tool is to simplify local development for projecct, that you also store in GitLab.
Very often you have to deal with a great amount of environment variables which are required for the operations in
GitLab CI. 

This script will help you to maintain your GitLab repository as a single source of truth for your environment variables.
It will pull the GitLab variables from the specified repository and its groups and export them to your local environment.

##Supported shells

 - bash
 - zhsell

##Installation

You can install the script by cloning this repo and executing ```pip install -e .```
from its root. Official PyPi registration is planned in the near future.
**Because of the nature of child processes on Unix based systems, the application will modify your shell configuration file.**
More info on why this is needed can be found here:
https://unix.stackexchange.com/questions/38205/change-environment-of-a-running-process

**You have to source your config file after running pip install by executing**
```source <your-shell-config-file>``` e.g. ```source .bashrc``` from your home directory.

## Configuration

###Global configuration
The global configuration file stores the repository endpoints with the access credentials. It can be found 
in ```~/.pyslurp/config.yml``` an will look as follows:
```yaml
sources:
  gitlab:
    - token: <your-gitlab-token>
      url: https://your.gitlab.host.url/
```

### Sample local config file
This configuration file must exist in every directory from which you want to call **pyslurp**
If you have distinct environment setups among your variables, you can specify the environment
you want in the corresponding field. By default, the "default" environment will be used.
```yaml
gitlab:
  url: https://your.gitlab.host.url/
  project_path : path/to/your/project
  environment: '*'
```
For GitLab repositories you can generate this file by running 
```pyslurp configuration autoconfig```
If no token configuration is found in the global config for the URL, a prompt for a
token will appear during configuration creation.

##Usage

In order to export the variables to your local environment, execute
```pyslurp gitlab shell``` in your terminal.
If you need semicolon separated values for your IDE instead, execute ```pyslurp gitlab shell```. 