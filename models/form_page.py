import os
from highlighter import Highlighter
import jsonpickle

from models.rectangle import Rectangle
from models.answer_box import GroupOfAnswers


class FormPage:
    image = None
    image_path: str
    json_path: str
    groups: list[GroupOfAnswers]
    default_group: GroupOfAnswers

    def __init__(self, path: str):
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.groups = list()
        self.default_group = GroupOfAnswers('default', Rectangle())
        self.groups.append(self.default_group)

    def to_json(self):
        j = jsonpickle.encode(self.groups, indent=4)
        with open(self.json_path, 'w') as file:
            file.write(j)

    def from_json(self):
        if not os.path.exists(self.json_path):
            self.from_image()
        self.groups = jsonpickle.decode(self.description())
        self.default_group = self.groups[0]

    def from_image(self):
        highlighter = Highlighter(self.image_path)
        highlighter.detect_boxes()
        self.default_group.contents = highlighter.boxes
        self.to_json()

    def description(self):
        with open(self.json_path, 'r') as file:
            return file.read()

    def describe_selected_groups(self):
        content: list = jsonpickle.decode(self.description())
        content.pop(0)
        return jsonpickle.encode(content, indent=4)

