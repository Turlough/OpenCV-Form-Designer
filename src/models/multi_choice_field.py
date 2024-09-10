from dataclasses import dataclass

from src.models.base_field import BaseField
from src.models.other_fields import BaseField, TickBox


@dataclass
class MultiChoice(BaseField):
    contents: list[TickBox]

    def __init__(self, in_sequence, out_sequence, name, rectangle):
        super().__init__(in_sequence, out_sequence, name, rectangle)
        self.contents = list()
