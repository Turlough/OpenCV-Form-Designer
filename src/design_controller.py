import os.path
from collections import deque
from enum import Enum, auto

from tabulate import tabulate

from src.models.designer.group_of_answers import GroupOfAnswers
from src.tools.highlighter import Highlighter
from src.models.rectangle import Rectangle
from src.models.designer.form_page import FormPage
from src.models.designer.answer_box import AnswerBox, RadioButton, RadioGroup
from src.views.designer.base_design_view import BaseDesignView


class EditMode(Enum):
    CREATE_BOX = auto()
    BOX_GROUP = auto()
    BOX_EDIT = auto()
    RADIO_GROUP = auto()
    NONE = auto()


class DesignController:
    page: FormPage
    scale: float
    edit_mode: EditMode = EditMode.NONE
    paths: deque[str]
    image_path: str
    json_path: str
    sequence_path: str
    highlighter: Highlighter
    views: list[BaseDesignView]

    def __init__(self, paths, scale):
        self.scale = scale
        self.paths = deque()
        self.views = list()
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
        self.sequence_path = path.replace('.tif', '.csv')

        if os.path.exists(self.json_path):
            self.load_from_json()
        else:
            self.page = FormPage(path)
        self.build_views(self.page)

    def set_mode(self, mode: EditMode):
        self.edit_mode = mode

    def create_answer(self, rect):
        x1, y1, x2, y2 = rect.topLeft().x(), rect.topLeft().y(), rect.bottomRight().x(), rect.bottomRight().y()
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rect = Rectangle().from_corners(x1, y1, x2, y2)
        sequence = len(self.page.answers) + 1
        answer = AnswerBox(sequence, sequence, f'A{sequence:0>2}', rect)
        self.page.answers.append(answer)
        self.build_views(self.page)

    def on_radio_group_drawn(self, name, x1, y1, x2, y2):
        sequence = len(self.page.answers) + 1
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rectangle = Rectangle().from_corners(x1, y1, x2, y2)
        group = RadioGroup(sequence, sequence, name, rectangle)
        contents = [answer for answer in self.page.answers if answer.rectangle.is_in(group.rectangle)]
        for c in contents:
            b = RadioButton(c.in_seq, c.out_seq, c.name, c.rectangle, group)
            group.buttons.append(b)
            self.page.answers.remove(c)
        self.page.answers.append(group)
        self.build_views(self.page)

    def on_group_box_drawn(self, name, x1, y1, x2, y2):
        sequence = len(self.page.groups) + 1
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rectangle = Rectangle().from_corners(x1, y1, x2, y2)
        group = GroupOfAnswers(sequence, sequence, name, rectangle)

        group.contents = [answer for answer in self.page.answers if answer.rectangle.is_in(group.rectangle)]
        self.page.groups.append(group)
        self.build_views(self.page)

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
            self.page.sort_by_csv()
        self.page.answers.sort(key=lambda a: a.in_seq)
        self.page.groups.sort(key=lambda g: g.in_seq)
        self.build_views(self.page)

    def save_to_json(self):
        self.page.answers.sort(key=lambda a: a.in_seq)
        self.page.groups.sort(key=lambda g: g.in_seq)
        with open(self.json_path, 'w') as file:
            file.write(self.page.to_json())
        with open(self.sequence_path, 'w') as file:
            for a in self.page.answers:
                row = f'{a.name},{a.in_seq},{a.out_seq}'
                file.write(row + '\n')

    def detect_rectangles(self):
        self.page.answers.clear()
        rectangles = self.highlighter.detect_boxes()
        for i, r in enumerate(rectangles):
            name = f'A{i + 1:0>2d}'
            a = AnswerBox(i + 1, i + 1, name, r)
            self.page.answers.append(a)
        self.build_views(self.page)

    def build_views(self, page):
        self.views.clear()
        for a in page.answers:
            # TODO: will this create the right type?
            v = BaseDesignView(a, self.scale)
            self.views.append(v)

    def list_index_values(self):
        response = list()
        headers = 'Name', 'Value'
        for r in self.views:
            name = r.model.name
            sequence = r.model.in_seq
            response.append((name, sequence))
        return tabulate(response, headers=headers, tablefmt="psql")
