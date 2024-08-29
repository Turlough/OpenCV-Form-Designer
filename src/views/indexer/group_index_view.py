import logging

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QHBoxLayout, QInputDialog, QMainWindow, QPushButton, \
    QWidget, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QCursor, QPixmap, QImage
from PyQt6.QtGui import QFont

from src.index_controller import IndexController
from src.models.designer.answer_box import AnswerBox
from src.views.indexer.index_label import ImageView

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class IndexView(QWidget):
    controller: IndexController
    edit: QTextEdit
    scroll_area: QScrollArea
    picture: ImageView

    def __init__(self, controller: IndexController):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.edit = QTextEdit()
        self.picture = ImageView(controller=controller)
        super().__init__()
        self.picture.page = controller.page

    def init_ui(self):
        """
        Layout UI elements
        """
        window = QMainWindow()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        main_layout = QHBoxLayout()
        image_button_layout = QHBoxLayout()

        # Main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        window.setCentralWidget(widget)
        # Left and right panels
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        # Image buttons top left
        left_layout.addLayout(image_button_layout)

        # Image area bottom left
        self.add_scroll_area_for_image(left_layout)

        next_button = QPushButton()
        next_button.setText('Next')
        next_button.clicked.connect(self.next_page)
        image_button_layout.addWidget(next_button)
        # left_layout.addLayout(bottom_layout)
        # right hand side
        right_layout.addWidget(self.edit)
        font = QFont()
        font.setPointSize(20)
        self.edit.setFont(font)

        self.setLayout(main_layout)

        image = self.controller.get_image()
        self.display(image)
        self.show_json()

    def show_json(self):
        self.edit.setText(self.controller.page.to_json())

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

    def on_click(self, rect: QRect):
        ...

    def reload(self):
        self.show_json()
        self.picture.draw_answers()
        # self.picture.draw_groups()

    def next_page(self):
        self.controller.next()
        image = self.controller.get_image()
        self.picture.page = self.controller.page
        self.display(image)

    def on_index_submitted(self, answer: AnswerBox, value: str):
        pass
