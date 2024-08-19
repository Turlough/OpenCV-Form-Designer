from highlighter import Highlighter
from models.box import Box
from models.form_page import FormPage
from models.tickbox import TickBoxGroup


class Controller:
    page: FormPage
    highlighter: Highlighter
    scale: float

    def __init__(self, path, scale):
        self.page = FormPage(path)
        self.scale = scale
        self.highlighter = Highlighter(path)
        self.page.from_json()

    def on_group_box_drawn(self, name, x1, y1, x2, y2):
        x1 /= self.scale
        y1 /= self.scale
        x2 /= self.scale
        y2 /= self.scale
        box = Box().from_corners(x1, y1, x2, y2)
        group = TickBoxGroup(name, box)
        group.contents = [tb for tb in self.page.default_group.contents if tb.box.is_in(group.rectangle)]
        self.page.box_groups.append(group)
        self.highlighter.add_tickbox_group(group)
        self.page.to_json()

    def get_image(self):
        self.highlighter.detect_boxes()
        return self.highlighter.scaled_and_highlighted(scale=self.scale)

    def get_text(self):
        return self.page.describe_groups()

