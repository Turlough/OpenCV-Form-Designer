from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.designer.answer_box import TickBox
from src.tools import colors
from src.views.designer.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TickBoxIndexView(BaseIndexView):
    model: TickBox
    ticked: bool = False
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)

    def __init__(self, model, text, scale, on_item_indexed, widget):
        super().__init__(model, text, scale, on_item_indexed, widget)
        if text.lower() == 'yes':
            self.ticked = True

    def draw_rectangle(self, painter):
        if self.ticked:
            painter.setBrush(colors.active_button)
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        self.pen = QPen(colors.index, 2)
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        desc = self.model.name
        tick_mark = '\u2714 Yes' if self.ticked else ''
        self.text = 'Yes' if self.ticked else ''

        painter.drawText(x, y, tick_mark)

    def on_click(self, painter, location):
        self.ticked = not self.ticked
        self.draw(painter)
