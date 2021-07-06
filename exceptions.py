"""PySlurp exceptions"""

class ConfigNotFoundException(Exception):
    """Throw if config file or element is not found"""

class ConfigInvalidException(Exception):
    """Throw if configuration is malformed"""

class GitProjectNotFoundException(Exception):
    """Throw if Git project was not found on remote"""

class GitGroupNotFoundException(Exception):
    """Throw if Git group was not found on remote"""

class ApiCheckFailedException(Exception):
    """Throw if expected REST API was not responsive on remote"""

class UnsupportedShellException(Exception):
    """Throw if user shell is not supported by pyslurp"""
