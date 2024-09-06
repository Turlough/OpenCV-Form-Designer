from typing import Any, Callable

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_base import AnswerBase


class BaseIndexView:
    model: AnswerBase
    text: str
    scale: float
    pen: QPen = QPen(Qt.GlobalColor.darkGreen, 2)
    rectangle: QRect
    on_item_indexed: Callable[['AnswerBase'], None]

    def __init__(self, model, text, scale, on_item_indexed: Callable):
        self.model = model
        self.text = text
        self.scale = scale
        self.on_item_indexed = on_item_indexed

        ((x1, y1), (x2, y2)) = model.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def draw_rectangle(self, painter):
        painter.setPen(self.pen)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        pass

    def on_click(self, painter, location: QPoint):
        pass
