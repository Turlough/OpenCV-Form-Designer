from dataclasses import dataclass

from src.models.base_field import BaseField

@dataclass
class TextBox(BaseField):
    pass


@dataclass
class NumberBox(TextBox):
    pass


@dataclass
class TickBox(BaseField):
    pass


@dataclass
class RadioButton(TickBox):

    def __init__(self, in_seq, out_seq, name, rectangle, group):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.group = group
        self.buttons: list[RadioButton] = list()


@dataclass
class RadioGroup(BaseField):
    def __init__(self, in_seq, out_seq, name, rectangle):
        super().__init__(in_seq, out_seq, name, rectangle)
        self.buttons: list[RadioButton] = list()
