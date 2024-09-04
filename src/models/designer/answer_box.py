from dataclasses import dataclass

from src.models.designer.answer_base import AnswerBase


@dataclass
class AnswerBox(AnswerBase):
    pass


@dataclass
class TextBox(AnswerBase):
    pass


@dataclass
class NumberBox(TextBox):
    pass


@dataclass
class TickBox(AnswerBox):
    pass


@dataclass
class RadioButton(TickBox):

    def __init__(self, in_seq, out_seq, name, rectangle, group):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.group = group
        self.buttons: list[RadioButton] = list()


@dataclass
class RadioGroup(AnswerBox):
    def __init__(self, in_seq, out_seq, name, rectangle):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.buttons: list[RadioButton] = list()
