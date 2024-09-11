from dataclasses import dataclass
import jsonpickle
from src.models.rectangle import Rectangle


@dataclass
class BaseField:
    name: str
    rectangle: Rectangle

    def to_json(self):
        return jsonpickle.encode(self, indent=4)

    @classmethod
    def from_json(cls, json_str):
        return jsonpickle.decode(json_str)

    def cast(self, new_class):
        """Cast the current object as another BaseField subclass"""
        return new_class(self.name, self.rectangle)
