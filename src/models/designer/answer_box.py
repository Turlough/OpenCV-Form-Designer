from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK


@dataclass
class TickBox(AnswerBox):
    type: BoxType = BoxType.TICK


@dataclass
class RadioGroup(AnswerBox):
    def __init__(self, in_seq, out_seq, name, rectangle):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.buttons: list[TickBox] = list()
