from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import RadioGroup
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.index_view_factory import IndexViewFactory


class RadioGroupIndexView(BaseIndexView):
    model: RadioGroup
    scale: float
    pen = QPen(Qt.GlobalColor.darkYellow, 2)
    button_views = list()

    def __init__(self, model, text, scale, on_item_indexed):
        super().__init__(model, text, scale, on_item_indexed)
        self.button_views = list()
        factory = IndexViewFactory(scale, self.on_item_indexed)
        for b in self.model.buttons:
            view = factory.create_button_for_group(b, '', self)
            self.button_views.append(view)

        for view in self.button_views:
            view.ticked = False
            view.text = ''
            if view.model.name == self.text:
                view.ticked = True
                view.text = view.model.name

    def draw(self, painter):
        super().draw(painter)
        for bv in self.button_views:
            bv.draw(painter)

    def button_clicked(self):
        pass

    def on_click(self, painter, location):
        x, y = location.x(), location.y()
        for b in self.button_views:
            b.ticked = False
            r = b.rectangle
            if r.left() < x < r.right() and r.top() < y < r.bottom():
                b.ticked = True
                self.text = b.model.name
                self.on_item_indexed()
            b.draw(painter)

