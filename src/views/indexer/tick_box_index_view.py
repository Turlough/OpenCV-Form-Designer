from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import TickBox
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TickBoxIndexView(BaseIndexView):
    model: TickBox
    ticked: bool = False
    scale: float
    pen = QPen(colors.tick, 1, Qt.PenStyle.DotLine)

    def __init__(self, model, text, scale, on_item_indexed, widget):
        super().__init__(model, text, scale, on_item_indexed, widget)
        if text.lower() == 'yes':
            self.ticked = True
        self.text = 'Yes' if self.ticked else ''

    def draw_text(self, painter):
        super().draw_text(painter)

    def draw_rectangle(self, painter):
        style = Qt.PenStyle.SolidLine if self.ticked else Qt.PenStyle.DotLine
        self.pen = QPen(colors.tick, 1, style)
        if self.ticked:
            painter.setBrush(colors.active_button)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)

    def on_click(self, painter, location):
        self.ticked = not self.ticked
        self.text = 'Yes' if self.ticked else ''
        self.draw(painter)
