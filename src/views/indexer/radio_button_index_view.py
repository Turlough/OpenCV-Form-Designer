from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from src.models.indexer.radio_group_response import RadioButtonResponse
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButtonResponse
    scale: float
    pen = QPen(Qt.GlobalColor.darkYellow, 2)

    def draw_rectangle(self, painter):
        color = QColor(200, 200, 75, 80)
        if self.model.ticked:
            painter.setBrush(color)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)





