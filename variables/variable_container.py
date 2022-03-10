"""Compartment for different variable categories"""

from typing import List

from variables.variable import Variable


def _add_to_container(container: dict, variables: dict):
    for key in variables.keys():
        container[key] = variables[key]


class VariableContainer:
    """Compartment for different variable categories"""
    __defaults = {}
    __source = {}
    __overrides = {}
    __joined_vars = {}

    def __init__(self):
        pass

    def add_source(self, variables: List[Variable]):
        """Add set of variables to the source dict"""
        _add_to_container(self.__source, variables)

    def add_defaults(self, variables: List[Variable]):
        """Add set of variables to the defaults dict"""
        _add_to_container(self.__defaults, variables)

    def add_overrides(self, variables: List[Variable]):
        """Add set of variables to the overrides dict"""
        _add_to_container(self.__overrides, variables)

    def get_vars(self):
        """
        Get all variables joined in a list.
        Variables from 'source' will override the 'defaults'
        Variables from 'overrides' will override everything else
        """
        _add_to_container(self.__joined_vars, self.__defaults)
        _add_to_container(self.__joined_vars, self.__source)
        _add_to_container(self.__joined_vars, self.__overrides)
        return list(self.__joined_vars.values())
