from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from src.index_controller import IndexController
from src.models.designer.form_page import FormPage
from src.models.indexer.response_base import ResponseBase
from src.views.designer.answer_box_painter import draw_answer, draw_group
from src.views.indexer.index_value_dialog import IndexDialog
from src.views.indexer.response_base_view import ResponseBaseView


class ImageView(QLabel):
    page: FormPage

    def __init__(self,  controller: IndexController, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.text = ''

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.update()

    def mouseMoveEvent(self, event):
        self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            answer: ResponseBaseView = self.controller.locate_surrounding_box(pos.x(), pos.y())
            if not answer:
                return
            answer.on_click(QPainter(self))

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_answers()
        self.draw_groups()

    def draw_answers(self):
        for a in self.controller.responses:
            a.draw(QPainter(self))
        self.update()

    def draw_groups(self):
        for g in self.page.groups:
            draw_group(g, QPainter(self), self.controller.scale)
        self.update()
