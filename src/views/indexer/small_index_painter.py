from typing import Callable

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from src.index_controller import IndexController
from src.models.form_page import FormPage
from src.views.indexer.base_index_view import BaseIndexView


class SmallIndexPainter(QLabel):
    page: FormPage
    field: BaseIndexView
    controller: IndexController
    on_item_indexed: Callable

    def __init__(self, controller: IndexController, parent=None, on_item_indexed=None):
        super().__init__(parent)
        self.controller = controller
        self.on_item_indexed = on_item_indexed

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update()

    def mouseMoveEvent(self, event):
        self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            view: BaseIndexView = self.controller.locate_surrounding_box(pos.x(), pos.y())
            if not view:
                return
            view.on_click(QPainter(self), pos)
            self.on_item_indexed(view)
