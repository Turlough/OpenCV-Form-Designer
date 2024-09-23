from typing import Callable

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QFont, QPen
from PyQt6.QtWidgets import QWidget

from src.models.base_field import BaseField
from src.tools import colors
from src.tools.global_functions import center_right


class BaseIndexView:
    model: BaseField
    text: str
    scale: float
    pen: QPen = QPen(colors.base_color, 2)
    font = QFont("Arial", 11)
    rectangle: QRect
    on_item_indexed: Callable[['BaseField'], None]
    parent_widget: QWidget

    def __init__(self, model, text, scale, on_item_indexed: Callable, widget):
        self.model = model
        self.text = text
        self.scale = scale
        self.on_item_indexed = on_item_indexed
        self.parent_widget = widget
        # The view rectangle is scaled up/down from the model rectangle. Also, it is a QRect.
        ((x1, y1), (x2, y2)) = model.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def highlight(self, painter):
        brush = QBrush(colors.selected)
        painter.setBrush(brush)
        painter.drawRect(self.rectangle)

    def draw_rectangle(self, painter):
        translucent = self.pen.color()
        translucent.setAlpha(10)
        painter.setBrush(QBrush(translucent))
        painter.setPen(self.pen)
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        margin = 2
        rect = self.get_text_rectangle(painter, self.text, margin)
        # Paint the background. First, translucent white
        painter.setPen(Qt.PenStyle.NoPen)
        brush = QBrush(colors.translucent)
        painter.setBrush(brush)
        painter.drawRect(rect)
        # And overlay with default color
        translucent = self.pen.color()
        translucent.setAlpha(10)
        brush = QBrush(translucent)
        painter.setBrush(brush)
        painter.drawRect(rect)
        translucent = self.pen.color()
        translucent.setAlpha(150)
        painter.setPen(translucent)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topRight(), rect.bottomRight())
        # Draw the text
        painter.setPen(QPen(colors.index, 1))
        bl = rect.bottomLeft()
        loc = QPoint(bl.x() + margin, bl.y() - margin)
        painter.drawText(loc, self.text)
        # Restore the original pen
        painter.setPen(self.pen)

    def get_text_rectangle(self, painter, text, margin):
        painter.setFont(self.font)
        m = painter.fontMetrics()
        w, h = m.horizontalAdvance(text), m.height()
        x, y = center_right(self.rectangle, h)
        x -= margin
        y += margin
        w += margin * 2
        h += margin * 2
        return QRect(x, y - h, w, h)

    def on_click(self, painter, location: QPoint):
        self.on_item_indexed()
