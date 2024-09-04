from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.indexer.radio_group_response import RadioGroupResponse
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.radio_button_index_view import RadioButtonIndexView


class RadioGroupIndexView(BaseIndexView):
    model: RadioGroupResponse
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)
    buttons: list[RadioButtonIndexView]

    def __init__(self, model, scale, callback):
        super().__init__(model, scale, callback)
        self.buttons = list()
        for b in self.model.button_responses:
            self.buttons.append(RadioButtonIndexView(b, scale, self.on_button_clicked))

    def on_button_clicked(self, button):
        for b in self.buttons:
            if b == button:
                self.model.text = b.model.question.name
                self.on_item_indexed(self.model)
                return

    def draw(self, painter):
        super().draw(painter)
        for bv in self.buttons:
            bv.draw(painter)
