from tabulate import tabulate
from collections import deque

from src.index_file_manager import IndexFileManager
from src.template_manager import TemplateManager
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
    file_manager: IndexFileManager
    template_manager: TemplateManager

    def __init__(self, template_folder, scale, index_path):
        self.scale = scale
        self.template_manager = TemplateManager(template_folder)
        self.file_manager = IndexFileManager(index_path)
        self.file_manager.read_all()
        self.views = list()
        self.next()

    def next(self):
        page_no = self.file_manager.page_number
        image = self.file_manager.get_page_image()
        self.highlighter = Highlighter.from_np_array(image)
        j, _ = self.template_manager.get_template(page_no)
        self.json_path = j
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
        for i, a in enumerate(page.answers):
            index = self.file_manager.load_index_value(i)
            factory = IndexViewFactory(self.scale, on_index_completed=self.save_index_value)
            v: BaseIndexView = factory.create_view(a, index)
            self.views.append(v)

    def save_index_value(self):
        values = [view.model.text for view in self.views]
        self.file_manager.save_page_indexes(values)

    def list_index_values(self):
        response = list()
        headers = '#', 'Field', 'Index Value'
        for i, r in enumerate(self.views):
            name = r.model.question.name
            text = r.model.text
            response.append((i + 1, name, text))
        return tabulate(response, headers=headers, tablefmt="fancy_grid")
