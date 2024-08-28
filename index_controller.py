import os.path
from collections import deque
from enum import Enum, auto

from tools.highlighter import Highlighter
from models.rectangle import Rectangle
from models.form_page import FormPage
from models.answer_box import AnswerBox, GroupOfAnswers


class IndexController:
    page: FormPage
    scale: float
    image_path: str
    json_path: str
    highlighter: Highlighter

    def __init__(self, paths, scale):
        self.scale = scale
        self.paths = deque()
        for p in paths:
            self.paths.append(p)
        self.next()

    def next(self):
        if not self.paths:
            return
        path = self.paths.popleft()
        self.image_path = path
        self.highlighter = Highlighter(path)
        self.json_path = path.replace('.tif', '.json')

        if os.path.exists(self.json_path):
            self.load_from_json()
        else:
            self.page = FormPage(path)

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y):
        x, y, _, _ = self.unscale(x, y)
        for answer in self.page.answers:
            r = answer.rectangle
            if r.x1 <= x <= r.x2 and r.y1 <= y <= r.y2:
                return answer
        return None

    def get_image(self):
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def load_from_json(self):
        with open(self.json_path, 'r') as file:
            content = file.read()
            self.page = FormPage.from_json(content)

    def save_to_json(self):
        with open(self.json_path, 'w') as file:
            file.write(self.page.to_json())

    def detect_rectangles(self):
        self.page.answers.clear()
        rectangles = self.highlighter.detect_boxes()
        for i, r in enumerate(rectangles):
            name = f'Answer{i:0>3d}'
            a = AnswerBox(name, r)
            self.page.answers.append(a)

    def index(self, answer, text):
        pass
