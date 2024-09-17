from PyQt6.QtGui import QPen

from src.models.other_fields import RadioGroup
from src.tools import colors
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.index_view_factory import IndexViewFactory


class RadioGroupIndexView(BaseIndexView):
    model: RadioGroup
    scale: float
    pen = QPen(colors.radio, 2)
    button_views = list()

    def __init__(self, model, text, scale, on_item_indexed):
        super().__init__(model, text, scale, on_item_indexed, None)
        self.button_views = list()
        factory = IndexViewFactory(scale, self.on_item_indexed)
        for b in self.model.buttons:
            view = factory.create_button_for_group(b, '', self)
            self.button_views.append(view)

        for view in self.button_views:
            view.ticked = False
            view.text_box = ''
            if view.model.name == self.text:
                view.ticked = True
                view.text_box = view.model.name

    def draw(self, painter):
        super().draw(painter)
        for bv in self.button_views:
            bv.draw(painter)

    def draw_text(self, painter):
        # Nothing
        pass

    def on_click(self, painter, location):
        button = self.identify_button(location)
        if not button:
            return
        for b in self.button_views:
            if b == button:
                button.on_click(painter, location)
            else:
                b.ticked = False
        self.text = button.model.name if button.ticked else ''
        self.on_item_indexed()
        button.draw(painter)

    def identify_button(self, location):
        x, y = location.x(), location.y()
        for b in self.button_views:
            r = b.rectangle
            if r.left() < x < r.right() and r.top() < y < r.bottom():
                return b
        return None

    def highlight(self, painter):
        painter.setBrush(colors.selected)
        painter.drawRect(self.rectangle)
        for v in self.button_views:
            v.draw(painter)

