from dataclasses import dataclass
from enum import Enum, auto

from models.box import Box


class BoxType(Enum):
    TICK = auto()
    TEXT = auto()
    NUMBER = auto()


@dataclass
class TickBox:
    name: str
    box: Box
    type: str = BoxType.TICK.name


@dataclass
class TickBoxGroup:
    name: str
    rectangle: Box
    contents: list[TickBox]

    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        self.contents = list()
