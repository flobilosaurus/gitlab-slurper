class ConfigNotFoundException(Exception):
    pass

class ConfigInvalidException(Exception):
    pass

class ProjectNotFoundException(Exception):
    pass

class GroupNotFoundException(Exception):
    pass

class ApiCheckFailedException(Exception):
    pass

class UnsupportedShellException(Exception):
    pass