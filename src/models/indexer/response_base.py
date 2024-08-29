from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase
from src.models.designer.answer_box import AnswerBox


@dataclass
class ResponseBase:
    question: AnswerBase


@dataclass
class TickBoxResponse(ResponseBase):
    question: AnswerBox
    ticked: bool = False


@dataclass
class TextIndexResponse(ResponseBase):
    question: AnswerBox
    text: str = ''
