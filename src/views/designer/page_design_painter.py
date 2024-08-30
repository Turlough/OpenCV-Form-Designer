from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect

from src.design_controller import DesignController, EditMode
from src.views.designer.global_functions import draw_group


class PageDesignPainter(QLabel):
    scale: float = 1.0
    mode: EditMode = EditMode.NONE
    controller: DesignController

    def __init__(self, controller: DesignController, on_release=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.on_release = on_release
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.scale = controller.scale

    def mousePressEvent(self, event):
        if self.mode == EditMode.NONE:
            self.start_point = self.end_point = None
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.update()

    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point)
            self.update()

    def mouseReleaseEvent(self, event):
        if self.mode == EditMode.NONE:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point)
            self.update()
            self.start_point = None
            self.end_point = None
            self.on_release(self.rect)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.mode == EditMode.RADIO_GROUP and not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.darkYellow, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
            self.update()
        if self.mode == EditMode.BOX_GROUP and not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.red, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
            self.update()
        if self.mode == EditMode.CREATE_BOX and not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.blue, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
            self.update()
        self.draw_answers()
        self.draw_groups()

    def draw_answers(self):
        for a in self.controller.views:
            a.draw(QPainter(self))
        self.update()

    def draw_groups(self):
        painter = QPainter(self)
        for g in self.controller.page.groups:
            draw_group(g, painter, self.scale)
        self.update()
