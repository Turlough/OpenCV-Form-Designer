from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel


class ImageLabel(QLabel):
    pixmap: QPixmap

    def load_cv_image(self, cv_image):
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(cv_image.data.tobytes(), w, h, bytes_per_line, QImage.Format.Format_BGR888)
        self.pixmap = QPixmap(qt_image)

        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Calculate image size and position
        image_rect = QtCore.QRect(0, 0, self.pixmap.width(), self.pixmap.height())
        label_rect = self.rect()
        label_rect.center()  # Center the label within the widget
        image_rect.moveCenter(label_rect.center())

        # Adjust position to bottom left
        image_rect.moveBottomLeft(label_rect.bottomLeft())

        painter.drawPixmap(image_rect, self.pixmap)
