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
        text_x, text_y = center_right(self.rectangle, text_height)
        text = '\u2714' if self.model.ticked else ''
        painter.drawText(text_x, text_y, text)

    def on_click(self, painter):
        self.model.ticked = not self.model.ticked
        self.draw(painter)
