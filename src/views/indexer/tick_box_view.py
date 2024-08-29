from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.indexer.response_base import TickBoxResponse
from src.views.designer.answer_box_painter import center_right, color_for_answer
from src.views.indexer.response_base_view import ResponseBaseView


class TickBoxView(ResponseBaseView):
    model: TickBoxResponse
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)

    def __init__(self, model, scale):
        super().__init__(model, scale)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        tick_mark = '\u2714' if self.model.ticked else ''

        painter.drawText(x, y, tick_mark)

    def on_click(self, painter):
        self.model.tick()
        self.draw(painter)
