from typing import Any, Callable

from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from src.index_controller import IndexController
from src.models.designer.form_page import FormPage
from src.views.indexer.base_index_view import BaseIndexView


class PageIndexPainter(QLabel):
    page: FormPage
    controller: IndexController
    callback: Callable

    def __init__(self,  controller: IndexController, parent=None, callback=None):
        super().__init__(parent)
        self.controller = controller
        self.callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update()

    def mouseMoveEvent(self, event):
        self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            answer: BaseIndexView = self.controller.locate_surrounding_box(pos.x(), pos.y())
            if not answer:
                return
            answer.on_click(QPainter(self))
            self.callback()

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_answers()

    def draw_answers(self):
        for a in self.controller.views:
            a.draw(QPainter(self))
        self.update()

