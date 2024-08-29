from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.indexer.response_base import TextIndexResponse
from src.views.designer.answer_box_painter import center_right, color_for_answer
from src.views.indexer.response_base_view import ResponseBaseView


class IndexTextView(ResponseBaseView):
    model: TextIndexResponse
    text: str
    pen = QPen(Qt.GlobalColor.darkGreen, 2)

    def __init__(self, model, scale):
        super().__init__(model, scale)

    def on_click(self, painter):
        self.model.text = "Tested"
        self.draw(painter)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 16))
        # Calculate the height of the text
        m = painter.fontMetrics()
        text_height = m.height()
        text_x, text_y = center_right(self.rectangle, text_height)
        painter.drawText(text_x, text_y, self.model.text[:5])
