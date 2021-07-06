"""Holds dataclasses for variables pulled from sources"""
from typing import Dict

from dataclasses import dataclass


@dataclass
class Variable:
    """Unified class to hold key and value of a pulled variable"""
    key: str
    value: str
    metadata: Dict = None
