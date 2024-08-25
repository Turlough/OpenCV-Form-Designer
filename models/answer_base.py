from dataclasses import dataclass
from enum import Enum, auto
import json
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
        # Convert the object to a dictionary
        data = {
            'class_name': self.__class__.__name__,
            'attributes': self.__dict__
        }
        return json.dumps(data, indent=4)

    @classmethod
    def from_json(cls, json_str):
        # Load data from JSON string
        data = json.loads(json_str)
        # Get the class by name (assume it's in the same module)
        class_name = data['class_name']
        attributes = data['attributes']
        # Dynamically create an instance of the class
        instance = globals()[class_name](**attributes)
        return instance
