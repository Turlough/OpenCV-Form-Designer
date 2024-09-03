from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase
from src.models.designer.answer_box import AnswerBox


@dataclass
class ResponseBase:
    question: AnswerBase
    text: str = ''


@dataclass
class TickBoxResponse(ResponseBase):
    question: AnswerBox
    ticked: bool = False

    def tick(self):
        self.ticked = not self.ticked
        self.text = "True" if self.ticked else "False"


@dataclass
class TextIndexResponse(ResponseBase):
    question: AnswerBox
