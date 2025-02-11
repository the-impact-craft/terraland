from dataclasses import dataclass

from textual.message import Message


@dataclass
class MoveEvent:
    timestamp: float
    delta: int


@dataclass
class MoveResizingRule(Message):
    orientation: str
    delta: int
    previous_component_id: str
    next_component_id: str


@dataclass
class SelectResizingRule(Message):
    id: str


@dataclass
class ReleaseResizingRule(Message):
    id: str
