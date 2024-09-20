from typing import Callable

import pyperclip
from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtGui import QBrush, QCursor, QFont, QPen
from src.models.base_field import BaseField
from src.tools import colors
from src.tools.global_functions import center, center_left, center_right
from src.views.dialogs.index_value_dialog import TextDialog


class BaseDesignView:
    model: BaseField
    scale: float
    pen: QPen = QPen(colors.base, 1, Qt.PenStyle.DotLine)
    rectangle: QRect
    editor_callback: Callable

    def __init__(self, model, scale, editor_callback: Callable):
        self.model = model
        self.scale = scale
        self.editor_callback = editor_callback

        ((x1, y1), (x2, y2)) = model.rectangle.coordinates(scale=scale)
        self.rectangle = QRect(x1, y1, x2 - x1, y2 - y1)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)

    def draw_rectangle(self, painter):
        painter.setPen(self.pen)
        translucent = (self.pen.color())
        translucent.setAlpha(30)
        painter.setBrush(QBrush(translucent))
        painter.drawRect(self.rectangle)

    def on_click(self):
        s = pyperclip.paste()
        if isinstance(s, str):
            self.model.name = (s.replace('\r', ' ')
                               .replace('\n', ' ')
                               .replace('\t', ' ')
                                .replace('  ', ' ')
                               .strip())
            self.editor_callback()
        else:
            mouse_pos = QCursor.pos()
            editor = TextDialog(self.model, callback=self.editor_callback)
            editor.move(mouse_pos)
            editor.exec()

    def draw_text(self, painter):
        margin = 1
        rect = self.get_text_rectangle(painter, self.model.name, margin)
        # Paint the background. First, translucent white
        painter.setPen(Qt.PenStyle.NoPen)
        brush = QBrush(colors.translucent)
        painter.setBrush(brush)
        painter.drawRect(rect)
        # And overlay with default color
        translucent = self.pen.color()
        translucent.setAlpha(30)
        brush = QBrush(translucent)
        painter.setBrush(brush)
        painter.drawRect(rect)
        translucent = self.pen.color()
        translucent.setAlpha(150)
        painter.setPen(translucent)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        # Draw the text
        painter.setPen(QPen(colors.index, 1))
        bl = rect.bottomLeft()
        loc = QPoint(bl.x() + margin, bl.y() - margin)
        painter.drawText(loc, self.model.name)
        # Restore the original pen
        painter.setPen(self.pen)

    def get_text_rectangle(self, painter, text, margin):
        font = QFont("Arial", 8)
        # font.setBold(True)
        painter.setFont(font)
        m = painter.fontMetrics()
        w, h = m.horizontalAdvance(text), m.height()
        x, y = center_left(self.rectangle, w, h)
        x -= margin
        y += margin
        w += margin * 2
        h += margin * 2
        return QRect(x, y - h, w, h)
