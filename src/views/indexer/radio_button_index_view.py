from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from src.models.designer.answer_box import RadioButton
from src.tools import colors
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButton
    scale: float
    pen = QPen(colors.radio_group, 2)

    def __init__(self, model, text, scale, on_item_indexed, group):
        super().__init__(model, text, scale, on_item_indexed, None)
        self.group = group

    def draw_rectangle(self, painter):
        if self.ticked:
            painter.setBrush(colors.active_button)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)





