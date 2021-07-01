from typing import Dict, Any

from dataclasses import dataclass, field


@dataclass
class Variable:
    key: str
    value: str
    metadata: Dict = None
