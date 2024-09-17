from PyQt6.QtWidgets import QWidget
from tabulate import tabulate

from src.models.base_field import BaseField
from src.models.other_fields import RadioGroup
from src.tools import common
from src.tools.index_file_manager import IndexFileManager
from src.tools.template_manager import TemplateManager
from src.tools.highlighter import Highlighter
from src.models.form_page import FormPage
from src.views.indexer.index_view_factory import IndexViewFactory
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.radio_group_index_view import RadioGroupIndexView


class IndexController:
    page: FormPage
    scale: float
    template_path: str
    json_path: str
    csv_path: str
    highlighter: Highlighter
    views: list[BaseIndexView]
    file_manager: IndexFileManager
    template_manager: TemplateManager
    image_widget: QWidget
    current_view: BaseIndexView

    def __init__(self, template_folder, scale):
        self.scale = scale
        self.template_manager = TemplateManager(template_folder)
        self.views = list()

    def load_index_file(self, path):
        counts = self.template_manager.get_field_counts()
        self.file_manager = IndexFileManager(path, counts)
        self.file_manager.read_all()
        self.views = list()
        self.load_page()

    def load_page(self):
        page_no = self.file_manager.page_number
        image = self.file_manager.get_page_image()
        self.highlighter = Highlighter.from_np_array(image)
        j, path = self.template_manager.get_template(page_no)
        self.json_path = j
        self.template_path = path
        self.load_from_json()
        self.current_view = self.views[0]

    def crop_to_field(self, model: BaseField):
        return self.highlighter.crop(model.rectangle, common.little_widget_scale)

    def prev_page(self):
        self.file_manager.prev_page()
        self.load_page()

    def next_page(self):
        self.file_manager.next_page()
        self.load_page()

    def next_document(self):
        self.file_manager.next_row()
        self.load_page()

    def next_field(self):
        idx = self.views.index(self.current_view)
        if idx + 1 >= len(self.views):
            self.next_page()
        else:
            self.current_view = self.views[idx + 1]

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= common.widget_scale
        y1 /= common.widget_scale
        x2 /= common.widget_scale
        y2 /= common.widget_scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y) -> BaseIndexView | None:
        x, y, _, _ = self.unscale(x, y)
        for resp in self.views:
            r = resp.model.rectangle
            if r.x1 <= x <= r.x2 and r.y1 <= y <= r.y2:
                return resp
        return None

    def get_image(self):
        # return self.highlighter.scaled_and_translated(0.316, -20, 62)
        return self.highlighter.scaled_and_highlighted(self.scale)

    def load_from_json(self):
        with open(self.json_path, 'r') as file:
            content = file.read()
            self.page = FormPage.from_json(content)
            self.page.sort_by_csv(self.template_path)
        self.build_views(self.page)

    def build_views(self, page):
        self.views.clear()
        for i, f in enumerate(page.fields):
            index = self.file_manager.load_index_value(i)
            factory = IndexViewFactory(common.widget_scale, on_index_completed=self.save_index_values)
            if isinstance(f, RadioGroup):
                v = RadioGroupIndexView(f, index, common.widget_scale, self.save_index_values)
            else:
                v = factory.create_view(f, index, self.image_widget)
            self.views.append(v)

    def save_index_values(self):
        values = [view.text for view in self.views]
        self.file_manager.save_page_indexes(values)

    def list_index_values(self):
        response = list()
        headers = '#', 'Field', 'Index Value'
        for i, view in enumerate(self.views):
            name = view.model.name
            text = view.text
            response.append((i + 1, name, text))
        return tabulate(response, headers=headers, tablefmt="fancy_grid")
