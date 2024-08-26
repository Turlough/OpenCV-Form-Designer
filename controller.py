import os.path
from enum import Enum, auto

from tools.highlighter import Highlighter
from models.rectangle import Rectangle
from models.form_page import FormPage
from models.answer_box import AnswerBox, GroupOfAnswers


class EditMode(Enum):
    BOX_GROUP = auto()
    BOX_EDIT = auto()


class Controller:
    page: FormPage
    scale: float
    edit_mode: EditMode = EditMode.BOX_GROUP
    answers: list[AnswerBox]
    image_path: str
    json_path: str
    highlighter: Highlighter

    def __init__(self, path, scale):
        self.image_path = path
        self.highlighter = Highlighter(path)
        self.json_path = path.replace('.tif', '.json')
        self.scale = scale

        if os.path.exists(self.json_path):
            content = self.get_page_json()
            self.page = FormPage.from_json(content)
        else:
            self.page = FormPage(path)

        if self.page.groups:
            self.answers = self.page.groups[0].contents
        else:
            self.answers = list()

    def set_mode(self, mode: EditMode):
        self.edit_mode = mode

    def on_group_box_drawn(self, name, x1, y1, x2, y2):
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rectangle = Rectangle().from_corners(x1, y1, x2, y2)
        group = GroupOfAnswers(name, rectangle)
        group.contents = [answer for answer in self.answers if answer.rectangle.is_in(group.rectangle)]
        self.page.groups.append(group)
        self.highlighter.add_tickbox_group(group)
        self.page.to_json()

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y):
        x, y, _, _ = self.unscale(x, y)
        for answer in self.answers:
            r = answer.rectangle
            if r.x1 < x < r.x2 and r.y1 < y < r.y2:
                return answer
        return None

    def get_image(self):
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def get_page_json(self):
        with open(self.json_path, 'r') as file:
            return file.read()

    def save_json(self):
        self.page.to_json()

    def detect_rectangles(self):
        self.answers.clear()
        rectangles = self.highlighter.detect_boxes()
        for i, r in enumerate(rectangles):
            name = f'Ans {i:<3d}'
            a = AnswerBox(name, r)
            self.answers.append(a)
