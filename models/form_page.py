import json
import os
from tools.highlighter import Highlighter

from models.rectangle import Rectangle
from models.answer_box import AnswerBase, GroupOfAnswers


class FormPage(AnswerBase):
    image = None
    image_path: str
    json_path: str
    groups: list[GroupOfAnswers]

    def __init__(self, path: str):
        self.name = 'Form Page'
        self.rectangle = Rectangle().from_corners(0, 0, 0, 0)
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.groups = list()

    def to_json(self):
        serialized_list = [group.to_json() for group in self.groups]

        data = {
            'class_name': self.__class__.__name__,
            'attributes': {
                'rectangle': self.rectangle,
                'class_list': serialized_list
            }
        }
        j = json.dumps(data, indent=4)

        with open(self.json_path, 'w') as file:
            file.write(j)

    @classmethod
    def from_json(cls, json_str):

        data = json.loads(json_str)
        class_name = data['class_name']
        attributes = data['attributes']
        # Deserialize the class_list
        groups = [AnswerBase.from_json(item) for item in attributes.pop('groups')]
        instance = globals()[class_name](**attributes)
        instance.class_list = groups
        return instance

