from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.designer.answer_base import AnswerBase
from src.views.designer.answer_box_painter import center_right


class BaseDesignView:
    model: AnswerBase
    scale: float
    pen: QPen = QPen(Qt.GlobalColor.yellow, 2)
    rectangle: QRect

    def __init__(self, model, scale):
        self.model = model
        self.scale = scale

        ((x1, y1), (x2, y2)) = model.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def draw_rectangle(self, painter):
        painter.setPen(self.pen)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        text = f'{self.model.name}'
        painter.drawText(x, y, text)

    def on_click(self, painter):
        pass
