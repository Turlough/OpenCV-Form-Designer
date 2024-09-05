from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.indexer.radio_group_response import RadioGroupResponse
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.radio_button_index_view import RadioButtonIndexView


class RadioGroupIndexView(BaseIndexView):
    model: RadioGroupResponse
    scale: float
    pen = QPen(Qt.GlobalColor.darkYellow, 2)
    buttons: list[RadioButtonIndexView]

    def __init__(self, model, scale, on_item_indexed):
        super().__init__(model, scale, on_item_indexed)
        self.buttons = list()
        for b in self.model.button_responses:
            self.buttons.append(RadioButtonIndexView(b, scale, self.on_item_indexed))

    def draw(self, painter):
        super().draw(painter)
        for bv in self.buttons:
            bv.draw(painter)

    def on_click(self, painter, location):
        x, y = location.x(), location.y()
        for b in self.buttons:
            b.model.ticked = False
            r = b.rectangle
            if r.left() < x < r.right() and r.top() < y < r.bottom():
                b.model.ticked = True
                self.model.text = b.model.question.name
                self.on_item_indexed()
