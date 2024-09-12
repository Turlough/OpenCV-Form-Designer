from PyQt6.QtWidgets import QDialog, QLabel
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect

from src.design_controller import DesignController, EditMode
from src.tools import colors
from src.views.dialogs.type_change_dialog import TypeChangeDialog


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

        if event.button() == Qt.MouseButton.RightButton:
            x, y = event.pos().x(), event.pos().y()
            view = self.controller.locate_surrounding_box(x, y)
            if not view:
                return

            dialog = TypeChangeDialog()
            dialog.move(x, y)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.controller.change_type(view, dialog.return_value)
                self.on_release(self.rect)

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
        if self.mode == EditMode.CREATE_FIELD and not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(colors.create_field, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
        # self.draw_fields()

    def draw_fields(self):
        for v in self.controller.views:
            v.draw(QPainter(self))
        self.update()
