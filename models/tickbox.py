from dataclasses import dataclass

from models.box import Box


@dataclass
class TickBox:
    name: str
    box: Box


@dataclass
class TickBoxGroup:
    name: str
    rectangle: Box
    contents: list[Box]

    def __init__(self, name, rectangle):
        self.name = name
        self.rectangle = rectangle
        self.contents = list()

