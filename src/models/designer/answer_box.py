from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK


@dataclass
class TickBox(AnswerBox):
    type: BoxType = BoxType.TICK


@dataclass
class RadioButton(TickBox):
    type: BoxType

    def __init__(self, in_seq, out_seq, name, rectangle, group):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.group = group
        self.buttons: list[RadioButton] = list()


@dataclass
class RadioGroup(AnswerBox):
    def __init__(self, in_seq, out_seq, name, rectangle):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.buttons: list[RadioButton] = list()
