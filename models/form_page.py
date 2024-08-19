import os
from highlighter import Highlighter
import jsonpickle

from models.box import Box
from models.tickbox import TickBox, TickBoxGroup


class FormPage:
    image = None
    image_path: str
    json_path: str
    box_groups: list[TickBoxGroup]
    default_group: TickBoxGroup

    def __init__(self, path: str):
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.box_groups = list()
        self.default_group = TickBoxGroup('default', Box())
        self.box_groups.append(self.default_group)

    def to_json(self):
        j = jsonpickle.encode(self.box_groups, indent=4)
        with open(self.json_path, 'w') as file:
            file.write(j)

    def from_json(self):
        if not os.path.exists(self.json_path):
            self.from_image()
        self.box_groups = jsonpickle.decode(self.description())

    def from_image(self):
        highlighter = Highlighter(self.image_path)
        highlighter.detect_boxes()
        self.default_group.contents = highlighter.tick_boxes
        self.to_json()

    def description(self):
        with open(self.json_path, 'r') as file:
            return file.read()

    def describe_groups(self):
        content: list = jsonpickle.decode(self.description())
        content.pop(0)
        return jsonpickle.encode(content, indent=4)

