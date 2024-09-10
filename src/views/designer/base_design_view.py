from typing import Callable

import pyperclip
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QCursor, QFont, QPen
from src.models.base_field import BaseField
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.dialogs.index_value_dialog import TextDialog


class BaseDesignView:
    model: BaseField
    scale: float
    pen: QPen = QPen(colors.text, 2)
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
        painter.drawRect(self.rectangle)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        h = m.height()
        x, y = center_right(self.rectangle, h)
        painter.drawText(x, y, self.model.name)

    def on_click(self):
        s = pyperclip.paste()
        if s:
            self.model.name = s
            self.editor_callback()
        else:
            mouse_pos = QCursor.pos()
            editor = TextDialog(self.model, callback=self.editor_callback)
            editor.move(mouse_pos)
            editor.exec()
