import json
from dataclasses import dataclass

from models.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK


@dataclass
class GroupOfAnswers(AnswerBase):
    contents: list[AnswerBox]

    def __init__(self, name, rectangle):
        super.__init__(name, rectangle)
        self.contents = list()
