import logging

from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMainWindow, QMessageBox, QPushButton, QWidget, \
    QLabel, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QFont


logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class ImageViewer(QWidget):
    edit: QTextEdit
    btn_next: QPushButton
    btn_reload: QPushButton
    scroll_area: QScrollArea

    style_normal = '{ background-color: rgba(250, 255, 0, 0.1); }'
    style_action = '{ background-color: rgba(255, 0, 0, 0.1); }'
    style_go = '{ background-color: rgba(50, 255, 50, 0.4); }'

    def __init__(self):
        self.edit_connected = False
        self.label = None
        self.scroll_area = QScrollArea()

        super().__init__()

    def init_ui(self, path):
        """
        Layout UI elements
        """
        window = QMainWindow()
        right_layout = QVBoxLayout()
        main_layout = QHBoxLayout()


        self.add_scroll_area_for_image(self.scroll_area, main_layout)

        # Right Panel
        right_layout.addWidget(self.edit)
        # Main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        window.setCentralWidget(widget)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def set_text(self, text):
        self.edit.setText(text)

    def add_editor(self):
        # Create a text edit
        font = QFont()
        font.setPointSize(16)
        self.edit.setFont(font)

    def add_scroll_area_for_image(self, scroll_area, layout):
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(800)
        layout.addWidget(scroll_area)

    def display(self, image):
        # Set the Pixmap
        h, w, ch = image.shape
        label = QLabel()
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap(qt_image)
        label.setPixmap(pixmap)
        self.scroll_area.resize(pixmap.width(), pixmap.height())
        self.scroll_area.setWidget(label)
        return pixmap

