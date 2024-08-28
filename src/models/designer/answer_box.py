from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK

