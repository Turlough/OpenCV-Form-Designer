from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen

from src.models.designer.answer_box import RadioButton
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButton
    scale: float
    pen = QPen(Qt.GlobalColor.darkYellow, 2)

    def __init__(self, model, text, scale, on_item_indexed, group):
        super().__init__(model, text, scale, on_item_indexed)
        self.group = group

    def draw_rectangle(self, painter):
        color = QColor(200, 200, 75, 80)
        if self.ticked:
            painter.setBrush(color)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)





