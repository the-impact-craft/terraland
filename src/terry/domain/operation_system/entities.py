from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class OperationSystem:
    name: str
    version: str


@dataclass(frozen=True)
class Variable:
    name: str
    value: str | None


@dataclass(frozen=True)
class EnvVariableFilter:
    prefix: Optional[str | List[str]] = None
    suffix: Optional[str] = None
    contains: Optional[str] = None
    case_sensitive: bool = False
    exact_match: bool = False
