from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QRect


class ImageLabel(QLabel):
    def __init__(self, on_release=None, parent=None):
        super().__init__(parent)
        self.on_release = on_release
        self.start_point = None
        self.end_point = None
        self.rect = QRect()
        self.text = ''

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
            self.on_release(self.rect)
            # Reset for the next rectangle
            self.start_point = None
            self.end_point = None

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.rect.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.GlobalColor.red, 2)
            painter.setPen(pen)
            painter.drawRect(self.rect)


