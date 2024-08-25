import json
from dataclasses import dataclass

from models.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK


@dataclass
class GroupOfAnswers(AnswerBase):
    contents: list[AnswerBox]

    def __init__(self, name, rectangle):
        super.__init__(name, rectangle)
        self.contents = list()

    def to_json(self):
        # Convert each object in class_list to JSON
        serialized_list = [obj.to_json() for obj in self.contents]
        data = {
            'class_name': self.__class__.__name__,
            'attributes': {
                'x1'        : self.x1,
                'y1'        : self.y1,
                'x2'        : self.x2,
                'y2'        : self.y2,
                'class_list': serialized_list
            }
        }
        return json.dumps(data, indent=4)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        class_name = data['class_name']
        attributes = data['attributes']
        # Deserialize the contents
        contents = [AnswerBase.from_json(item) for item in attributes.pop('contents')]
        instance = globals()[class_name](**attributes)
        instance.class_list = contents
        return instance
