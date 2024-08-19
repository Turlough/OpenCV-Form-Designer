import logging

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLineEdit, QMainWindow, QMessageBox, QPushButton, \
    QWidget, \
    QLabel, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QFont

import highlighter
from controller import Controller
from image_label import ImageLabel

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class ImageViewer(QWidget):
    controller: Controller
    edit: QTextEdit
    scroll_area: QScrollArea
    picture: ImageLabel
    scale: float

    def __init__(self, controller: Controller):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.edit = QTextEdit()
        self.picture = ImageLabel(on_release=self.on_rectangle_drawn)
        super().__init__()

    def init_ui(self, path: str, scale: float):
        """
        Layout UI elements
        """
        self.scale = scale
        window = QMainWindow()
        right_layout = QVBoxLayout()
        main_layout = QHBoxLayout()

        self.add_scroll_area_for_image(main_layout)

        # Main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        window.setCentralWidget(widget)
        main_layout.addLayout(right_layout)
        right_layout.addWidget(self.edit)
        self.setLayout(main_layout)

        image = self.controller.get_image()
        self.display(image)

        self.set_text(self.controller.get_text())

    def set_text(self, text):
        self.edit.setText(text)

    def add_editor(self):
        # Create a text edit
        font = QFont()
        font.setPointSize(16)
        self.edit.setFont(font)

    def add_scroll_area_for_image(self, layout):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(800)
        layout.addWidget(self.scroll_area)

    def display(self, image):
        # Set the Pixmap
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap(qt_image)
        self.picture.setPixmap(pixmap)
        self.scroll_area.resize(pixmap.width(), pixmap.height())
        self.scroll_area.setWidget(self.picture)
        return pixmap

    def on_rectangle_drawn(self, rect: QRect):
        name, ok = QInputDialog.getText(self, 'Name', 'Type a name for this group')

        if not ok or not name:
            return

        x1, y1 = rect.topLeft().x(), rect.topLeft().y()
        x2, y2 = rect.bottomRight().x(), rect.bottomRight().y()

        self.controller.on_group_box_drawn(name, x1, y1, x2, y2)
        self.set_text(self.controller.get_text())

