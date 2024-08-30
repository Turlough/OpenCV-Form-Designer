from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.indexer.response_base import ResponseBase
from src.models.rectangle import Rectangle
from src.views.designer.global_functions import center_right, color_for_answer


class BaseIndexView:
    model: ResponseBase
    scale: float
    pen: QPen = QPen(Qt.GlobalColor.darkGreen, 2)
    rectangle: QRect

    def __init__(self, model, scale):
        self.model = model
        self.scale = scale

        ((x1, y1), (x2, y2)) = model.question.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def draw_rectangle(self, painter):
        painter.setPen(self.pen)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        pass

    def on_click(self, painter):
        pass
