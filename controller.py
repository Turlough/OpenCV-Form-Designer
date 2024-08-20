from enum import Enum, auto

from highlighter import Highlighter
from models.box import Box
from models.form_page import FormPage
from models.tickbox import TickBoxGroup


class EditMode(Enum):
    BOX_GROUP = auto()
    BOX_EDIT = auto()


class Controller:
    page: FormPage
    highlighter: Highlighter
    scale: float
    edit_mode: EditMode = EditMode.BOX_GROUP

    def __init__(self, path, scale):
        self.page = FormPage(path)
        self.scale = scale
        self.highlighter = Highlighter(path)
        self.page.from_json()
        for group in self.page.box_groups:
            self.highlighter.add_tickbox_group(group)

    def set_mode(self, mode: EditMode):
        self.edit_mode = mode

    def on_group_box_drawn(self, name, x1, y1, x2, y2):
        x1, y1, x2, y2 = self.unscale(x1, y1, x2, y2)
        box = Box().from_corners(x1, y1, x2, y2)
        group = TickBoxGroup(name, box)
        group.contents = [tb for tb in self.page.default_group.contents if tb.box.is_in(group.rectangle)]
        self.page.box_groups.append(group)
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
        for tickbox in self.page.default_group.contents:
            box = tickbox.box
            if box.x1 < x < box.x2 and box.y1 < y < box.y2:
                return tickbox
        return None

    def get_image(self):
        self.highlighter.detect_boxes()
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def get_page_json(self):
        return self.page.description()

    def write_to_json(self):
        self.page.to_json()

