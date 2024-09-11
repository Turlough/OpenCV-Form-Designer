from dataclasses import dataclass
from src.models.other_fields import BaseField, TickBox


@dataclass
class MultiChoice(BaseField):
    contents: list[TickBox]

    def __init__(self, name, rectangle):
        super().__init__(name, rectangle)
        self.contents = list()
