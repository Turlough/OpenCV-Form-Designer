import logging

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, \
    QWidget, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QFont

from src.index_controller import IndexController
from src.views.indexer.page_index_painter import PageIndexPainter

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class PageIndexView(QWidget):
    controller: IndexController
    edit: QTextEdit
    scroll_area: QScrollArea
    picture: PageIndexPainter

    def __init__(self, controller: IndexController):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.edit = QTextEdit()
        self.picture = PageIndexPainter(controller=controller, on_item_indexed=self.on_index_submitted)
        super().__init__()

    def init_ui(self):
        """
        Layout UI elements
        """
        window = QMainWindow()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        self.controller.image_widget = self
        self.controller.load_page()

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
        font = QFont('Courier', 10)
        # font.setPointSize(11)
        self.edit.setFont(font)

        self.setLayout(main_layout)
        self.picture.page = self.controller.page
        image = self.controller.get_image()
        self.display(image)
        self.update_text_area()

    def update_text_area(self):
        indexes = self.controller.list_index_values()
        self.edit.setText(indexes)

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

    def reload(self):
        self.update_text_area()
        self.picture.draw_answers()

    def next_page(self):
        self.controller.next()
        image = self.controller.get_image()
        self.picture.page = self.controller.page
        self.display(image)
        self.update_text_area()

    def on_index_submitted(self, model):
        self.reload()
