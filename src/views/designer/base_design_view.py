from typing import Callable

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QCursor, QFont, QPen

from src.models.designer.answer_base import AnswerBase
from src.views.designer.generic_model_editor import ModelEditor
from src.views.designer.global_functions import center_right


class BaseDesignView:
    model: AnswerBase
    scale: float
    pen: QPen = QPen(Qt.GlobalColor.yellow, 2)
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
        mouse_pos = QCursor.pos()
        editor = ModelEditor(self.model, callback=self.editor_callback)
        editor.move(mouse_pos)
        editor.exec()
