from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from src.index_controller import IndexController
from src.models.designer.form_page import FormPage
from src.views.designer.answer_box_painter import draw_answer, draw_group
from src.views.indexer.index_value_dialog import IndexDialog


class IndexLabel(QLabel):
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
            answer = self.controller.locate_surrounding_box(pos.x(), pos.y())
            if not answer:
                return
            (x1, y1), (x2, y2) = answer.rectangle.coordinates(self.controller.scale)
            dialog = IndexDialog(self)
            w, h = dialog.width(), dialog.height()
            dialog.move(x2 + w + 5, y2 + h - 5)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.controller.index(answer, dialog.lineEdit.text)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_answers()
        self.draw_groups()

    def draw_answers(self):
        painter = QPainter(self)
        for a in self.page.answers:
            draw_answer(a, painter, self.controller.scale)
        self.update()

    def draw_groups(self):
        painter = QPainter(self)
        for g in self.page.groups:
            draw_group(g, painter, self.controller.scale)
        self.update()
