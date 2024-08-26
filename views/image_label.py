from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect

from controller import EditMode
from models.answer_box import AnswerBox, BoxType
from views.answer_box_painter import draw


class ImageLabel(QLabel):
    answers: list[AnswerBox]
    scale: float = 1.0
    mode: EditMode = EditMode.NONE

    def __init__(self, scale=1.0, on_release=None, parent=None):
        super().__init__(parent)
        self.on_release = on_release
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.text = ''
        self.scale = scale
        self.answers = list()

    def mousePressEvent(self, event):
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

        if event.button() == Qt.MouseButton.LeftButton:
            self.end_point = event.pos()
            self.rect = QRect(self.start_point, self.end_point)
            self.update()
            self.text = f"Rectangle coordinates: {self.rect.topLeft()} to {self.rect.bottomRight()}"
            # Reset for the next coordinates
            self.start_point = None
            self.end_point = None
            self.on_release(self.rect)


    def paintEvent(self, event):
        super().paintEvent(event)
        if self.mode == EditMode.BOX_GROUP and not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.red, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)
        self.draw_answers()

    def draw_answers(self):
        painter = QPainter(self)
        for a in self.answers:
            draw(a, painter, self.scale)
        self.update()
