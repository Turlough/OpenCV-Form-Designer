import os.path
from collections import deque
from enum import Enum, auto

from tabulate import tabulate

from src.models.multi_choice_field import MultiChoice
from src.tools.highlighter import Highlighter
from src.models.rectangle import Rectangle
from src.models.form_page import FormPage
from src.models.other_fields import BaseField, RadioButton, RadioGroup
from src.views.designer.base_design_view import BaseDesignView
from src.views.designer.design_view_factory import DesignViewFactory


class EditMode(Enum):
    CREATE_FIELD = auto()
    EDIT_FIELD = auto()
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
        self.highlighter = Highlighter.from_path(path)
        self.json_path = path.replace('.jpg', '.json')
        self.sequence_path = path.replace('.jpg', '.csv')

        if os.path.exists(self.json_path):
            self.load_from_json()
        else:
            self.page = FormPage(path)
        self.build_views(self.page)

    def set_mode(self, mode: EditMode):
        self.edit_mode = mode

    def create_field(self, rect):
        x1, y1, x2, y2 = rect.topLeft().x(), rect.topLeft().y(), rect.bottomRight().x(), rect.bottomRight().y()
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rect = Rectangle().from_corners(x1, y1, x2, y2)
        seq = len(self.views) + 1
        field = BaseField(f'A{seq:0>2}', rect)
        self.page.fields.append(field)
        self.build_views(self.page)

    def on_radio_group_drawn(self, name, x1, y1, x2, y2):
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rectangle = Rectangle().from_corners(x1, y1, x2, y2)
        group = RadioGroup(name, rectangle)
        contents = [f for f in self.page.fields if f.rectangle.is_in(group.rectangle)]
        for c in contents:
            b = RadioButton(c.name, c.rectangle, group)
            group.buttons.append(b)
            self.page.fields.remove(c)
        self.page.fields.append(group)
        self.build_views(self.page)
        self.save_and_reload()

    def on_group_box_drawn(self, name, x1, y1, x2, y2):
        sequence = len(self.page.groups) + 1
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        rectangle = Rectangle().from_corners(x1, y1, x2, y2)
        group = MultiChoice(name, rectangle)

        group.contents = [f for f in self.page.fields if f.rectangle.is_in(group.rectangle)]
        self.page.groups.append(group)
        self.build_views(self.page)

    def unscale(self, x1, y1, x2=0, y2=0):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        return int(x1), int(y1), int(x2), int(y2)

    def locate_surrounding_box(self, x, y) -> BaseDesignView | None:
        # Deal with radio groups separately
        non_groups = filter(lambda v: not isinstance(v.model, RadioGroup), self.views)
        for view in non_groups:
            r = view.rectangle
            if r.left() <= x <= r.right() and r.top() <= y <= r.bottom():
                return view
        groups = filter(lambda v: isinstance(v.model, RadioGroup), self.views)
        for group in groups:
            # First check if a button was the target
            for view in group.button_views:
                r = view.rectangle
                if r.left() <= x <= r.right() and r.top() <= y <= r.bottom():
                    return view
            # Then check if the group is the target
            r = group.rectangle
            if r.left() <= x <= r.right() and r.top() <= y <= r.bottom():
                return group

        return None

    def get_image(self):
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def save_and_reload(self):
        self.save_to_json()
        self.load_from_json()

    def load_from_json(self):
        with open(self.json_path, 'r') as file:
            content = file.read()
            self.page = FormPage.from_json(content)
            self.page.sort_by_csv(self.image_path)
        self.build_views(self.page)

    def save_to_json(self):
        with open(self.json_path, 'w') as file:
            file.write(self.page.to_json())
        with open(self.sequence_path, 'w') as file:
            for f in self.page.fields:
                file.write(f.name + '\n')

    def detect_rectangles(self):
        self.page.fields.clear()
        rectangles = self.highlighter.detect_boxes()
        for i, r in enumerate(rectangles):
            name = f'A{i + 1:0>2d}'
            f = BaseField(name, r)
            self.page.fields.append(f)
        self.build_views(self.page)

    def build_views(self, page):
        self.views.clear()
        for f in page.fields:
            factory = DesignViewFactory()
            v = factory.create_view(f, self.scale, editor_callback=self.save_and_reload)
            self.views.append(v)

    def tabulate_view_models(self):
        response = list()
        headers = '#', 'Name', 'Class'
        for i, r in enumerate(self.views):
            name = r.model.name
            clz = r.model.__class__.__name__
            response.append((i + 1, name, clz))
        return tabulate(response, headers=headers, tablefmt="fancy_grid")

    def change_type(self, view: BaseDesignView, return_value):
        model = view.model
        new_model = model.cast(return_value)
        i = self.page.fields.index(model)
        self.page.fields[i] = new_model
        new_view = DesignViewFactory().create_view(new_model, self.scale, editor_callback=self.save_and_reload)
        i = self.views.index(view)
        self.views[i] = new_view
        self.save_and_reload()

