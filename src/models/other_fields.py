from dataclasses import dataclass

from src.models.base_field import BaseField


@dataclass
class TextBox(BaseField):
    pass


@dataclass
class LongTextBox(TextBox):
    pass


@dataclass
class NumberBox(TextBox):
    pass


@dataclass
class TickBox(BaseField):
    pass


@dataclass
class RadioButton(TickBox):

    def __init__(self, name, rectangle, group):
        super().__init__(name, rectangle)
        self.group = group
        self.buttons: list[RadioButton] = list()


@dataclass
class RadioGroup(BaseField):
    def __init__(self, name, rectangle):
        super().__init__(name, rectangle)
        self.buttons: list[RadioButton] = list()
