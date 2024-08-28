from dataclasses import dataclass

from models.answer_base import AnswerBase
from models.answer_box import AnswerBox


@dataclass
class GroupOfAnswers(AnswerBase):
    contents: list[AnswerBox]

    def __init__(self, name, rectangle):
        super().__init__(name, rectangle)
        self.contents = list()