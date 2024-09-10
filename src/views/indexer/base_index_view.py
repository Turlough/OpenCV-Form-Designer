from typing import Callable

from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QWidget

from src.models.base_field import BaseField
from src.tools import colors


class BaseIndexView:
    model: BaseField
    text: str
    scale: float
    pen: QPen = QPen(colors.base_color, 2)
    rectangle: QRect
    on_item_indexed: Callable[['BaseField'], None]
    parent_widget: QWidget

    def __init__(self, model, text, scale, on_item_indexed: Callable, widget):
        self.model = model
        self.text = text
        self.scale = scale
        self.on_item_indexed = on_item_indexed
        self.parent_widget = widget

        ((x1, y1), (x2, y2)) = model.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def highlight(self, painter):
        painter.setBrush(colors.selected)
        painter.drawRect(self.rectangle)

    def draw_rectangle(self, painter):
        painter.setPen(self.pen)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        pass

    def on_click(self, painter, location: QPoint):
        self.on_item_indexed()
