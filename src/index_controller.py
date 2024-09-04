from tabulate import tabulate
from collections import deque
from src.tools.highlighter import Highlighter
from src.models.designer.form_page import FormPage
from src.views.indexer.index_view_factory import IndexViewFactory
from src.views.indexer.base_index_view import BaseIndexView


class IndexController:
    page: FormPage
    scale: float
    image_path: str
    json_path: str
    csv_path: str
    highlighter: Highlighter
    views: list[BaseIndexView]

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
        self.load_from_json()

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y) -> BaseIndexView | None:
        x, y, _, _ = self.unscale(x, y)
        for resp in self.views:
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
            self.page.sort_by_csv()
        self.build_views(self.page)

    def build_views(self, page):
        self.views.clear()
        for a in page.answers:
            factory = IndexViewFactory()
            v = factory.create_view(a, self.scale, on_index_completed=lambda: self.save_index_value(a))
            self.views.append(v)

    def save_index_value(self, value):
        pass

    def list_index_values(self):
        response = list()
        headers = 'Name', 'Value'
        for r in self.views:
            name = r.model.question.name
            text = r.model.text
            response.append((name, text))
        return tabulate(response, headers=headers, tablefmt="psql")
