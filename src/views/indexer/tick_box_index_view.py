from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QBrush, QFont, QPen

from src.models.other_fields import TickBox
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TickBoxIndexView(BaseIndexView):
    model: TickBox
    ticked: bool = False
    scale: float
    pen = QPen(colors.tick, 1, Qt.PenStyle.DotLine)
    font = QFont("Arial", 8)

    def __init__(self, model, text, scale, on_item_indexed, widget):
        super().__init__(model, text, scale, on_item_indexed, widget)
        if text.lower() == 'yes':
            self.ticked = True
        self.text = 'Yes' if self.ticked else ''

    def draw_rectangle(self, painter):
        style = Qt.PenStyle.SolidLine if self.ticked else Qt.PenStyle.DotLine
        self.pen = QPen(colors.tick, 1, style)
        if self.ticked:
            painter.setBrush(colors.active_button)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        # Temporary value for drawing
        self.text = '\u2714' if self.ticked else ''
        super().draw_text(painter)
        # Reset to export form, 'Yes'
        self.text = 'Yes' if self.ticked else ''

    def on_click(self, painter, location):
        self.ticked = not self.ticked
        self.text = 'Yes' if self.ticked else ''
        self.draw(painter)
        self.on_item_indexed()
