from dataclasses import dataclass
from enum import Enum, auto

from models.rectangle import Rectangle


class BoxType(Enum):
    TICK = auto()
    TEXT = auto()
    NUMBER = auto()


@dataclass
class AnswerBox:
    name: str
    rectangle: Rectangle
    type: BoxType = BoxType.TICK


@dataclass
class GroupOfAnswers:
    name: str
    rectangle: Rectangle
    contents: list[AnswerBox]

    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        self.contents = list()
