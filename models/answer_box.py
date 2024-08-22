from dataclasses import dataclass
from enum import Enum, auto

from models.rectangle import Rectangle


class BoxType(Enum):
    TICK = auto()
    TEXT = auto()
    NUMBER = auto()


@dataclass
class AnswerBase:
    name: str
    rectangle: Rectangle


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK


@dataclass
class GroupOfAnswers(AnswerBase):
    contents: list[AnswerBox]

    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        self.contents = list()
