import os
from highlighter import Highlighter
import jsonpickle

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
        j = jsonpickle.encode(self.groups, indent=4)
        with open(self.json_path, 'w') as file:
            file.write(j)

    def from_json(self):
        if not os.path.exists(self.json_path):
            self.from_image()
        self.groups = jsonpickle.decode(self.read_file())

    def from_image(self):
        highlighter = Highlighter(self.image_path)
        highlighter.detect_boxes()
        self.to_json()

    def read_file(self):
        with open(self.json_path, 'r') as file:
            return file.read()
