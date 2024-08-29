import os.path
from collections import deque

from src.models.designer.answer_base import BoxType
from src.models.indexer.response_base import TextIndexResponse, ResponseBase, TickBoxResponse
from src.tools.highlighter import Highlighter
from src.models.designer.form_page import FormPage
from src.views.indexer.answer_box_view import IndexTextView
from src.views.indexer.response_base_view import ResponseBaseView
from src.views.indexer.tick_box_view import TickBoxView


class IndexController:
    page: FormPage
    scale: float
    image_path: str
    json_path: str
    highlighter: Highlighter
    responses: list[ResponseBaseView]

    def __init__(self, paths, scale):
        self.scale = scale
        self.paths = deque()
        self.responses = list()
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
        self.load_from_json()

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y) -> ResponseBaseView | None:
        x, y, _, _ = self.unscale(x, y)
        for resp in self.responses:
            r = resp.model.question.rectangle
            if r.x1 <= x <= r.x2 and r.y1 <= y <= r.y2:
                return resp
        return None

    def get_image(self):
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def load_from_json(self):
        with open(self.json_path, 'r') as file:
            content = file.read()
            self.page = FormPage.from_json(content)
        for ans in self.page.answers:
            match ans.type:
                case BoxType.TICK:
                    r = TickBoxResponse(ans, ticked=False)
                    rv = TickBoxView(r, self.scale)
                case _:
                    r = TextIndexResponse(ans)
                    rv = IndexTextView(r, self.scale)
            self.responses.append(rv)

    def save_to_json(self):
        with open(self.json_path, 'w') as file:
            file.write(self.page.to_json())

    def index(self, answer, text):
        pass
