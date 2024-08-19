import os
from highlighter import Highlighter
import jsonpickle
from models.tickbox import TickBox, TickBoxGroup


class FormPage:
    image = None
    image_path: str
    json_path: str
    tick_boxes: list[TickBox]
    box_groups: list[TickBoxGroup]

    def __init__(self, path: str):
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.tick_boxes = list()
        self.box_groups = list()

    def to_json(self):
        j = jsonpickle.encode(self.tick_boxes, indent=4)
        with open(self.json_path, 'w') as file:
            file.write(j)

    def from_json(self):
        if not os.path.exists(self.json_path):
            highlighter = Highlighter(self.image_path)
            highlighter.detect_boxes()
            self.tick_boxes = highlighter.tick_boxes
            self.to_json()
        with open(self.json_path, 'r') as file:
            content = file.read()
            self.tick_boxes = jsonpickle.decode(content)
