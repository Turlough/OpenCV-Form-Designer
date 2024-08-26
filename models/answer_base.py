from dataclasses import dataclass
from enum import Enum, auto
import jsonpickle
from models.rectangle import Rectangle


class BoxType(Enum):
    TICK = auto()
    TEXT = auto()
    NUMBER = auto()


@dataclass
class AnswerBase:
    name: str
    rectangle: Rectangle

    def to_json(self):
        return jsonpickle.encode(self)

    @classmethod
    def from_json(cls, json_str):
        return jsonpickle.decode(json_str)
