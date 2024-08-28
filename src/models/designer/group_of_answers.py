from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase
from src.models.designer.answer_box import AnswerBox


@dataclass
class GroupOfAnswers(AnswerBase):
    contents: list[AnswerBox]

    def __init__(self, in_sequence, out_sequence, name, rectangle):
        super().__init__(in_sequence, out_sequence, name, rectangle)
        self.contents = list()
