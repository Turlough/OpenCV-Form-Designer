import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QLayout, QMainWindow, QPushButton, \
    QScrollArea, QWidget, \
    QVBoxLayout, QTextEdit
from PyQt6.QtGui import QPixmap, QImage, QTextCursor
from PyQt6.QtGui import QFont

from src.index_controller import IndexController
from src.tools import common
from src.tools.logging_annotation import log_use
from src.views.indexer.index_widget import IndexWidget
from src.views.indexer.page_index_painter import PageIndexPainter


logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.INFO)


class PageIndexView(QWidget):
    controller: IndexController
    summary_area: QTextEdit
    scroll_area: QScrollArea
    picture: PageIndexPainter
    index_widget: IndexWidget

    def __init__(self, controller: IndexController):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.summary_area = QTextEdit()
        self.picture = PageIndexPainter(controller=controller, on_item_indexed=self.reload)

        super().__init__()

    @log_use
    def init_ui(self):
        """
        Layout UI elements
        """
        window = QMainWindow()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        # TODO- hack! fixme
        self.controller.image_widget = self

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
        # Main image display area is 'picture'
        self.add_scroll_area_for_image(left_layout)

        load_index_button = QPushButton()
        load_index_button.setText('Load Indexes')
        load_index_button.clicked.connect(self.open_file_dialog)
        image_button_layout.addWidget(load_index_button)

        next_doc_button = QPushButton()
        next_doc_button.setText('Next Questionnaire')
        next_doc_button.clicked.connect(self.next_document)
        image_button_layout.addWidget(next_doc_button)

        prev_page_button = QPushButton()
        prev_page_button.setText('Prev Page')
        prev_page_button.clicked.connect(self.prev_page)
        image_button_layout.addWidget(prev_page_button)

        next_page_button = QPushButton()
        next_page_button.setText('Next Page')
        next_page_button.clicked.connect(self.next_page)
        image_button_layout.addWidget(next_page_button)

        self.index_widget = IndexWidget(None, self.on_enter_key_used)
        right_layout.addWidget(self.index_widget)

        next_field_button = QPushButton()
        next_field_button.setText('Next Field')
        next_field_button.clicked.connect(self.next_field)
        right_layout.addWidget(next_field_button)

        right_layout.addWidget(self.summary_area)
        font = QFont('Courier', 10)
        self.summary_area.setFont(font)

        self.setLayout(main_layout)
        self.open_file_dialog()

    def update_summary_area(self):
        indexes = self.controller.list_index_values()
        self.summary_area.setText(indexes)

    def add_scroll_area_for_image(self, layout):
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

    @log_use
    def display(self, image):
        # Set the Pixmap
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap(qt_image)

        self.picture.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.picture.setPixmap(pixmap)

        self.picture.resize(pixmap.width(), pixmap.height())
        self.scroll_area.setWidget(self.picture)

    @log_use
    def reload(self):
        image = self.controller.get_image()
        self.picture.page = self.controller.page
        self.display(image)
        view = self.controller.current_view
        img = self.controller.crop_to_field(view.model)
        self.index_widget.display(view, img)
        self.update_summary_area()
        self.picture.draw_answers()
        title = self.controller.file_manager.current_document
        page = self.controller.file_manager.page_number + 1
        title = f'{title}  Page {page}'
        self.setWindowTitle(title)

    def prev_page(self):
        self.controller.prev_page()
        self.reload()

    def next_page(self):
        if self.controller.has_more_pages():
            self.controller.next_page()
            self.reload()
        else:
            self.next_document()

    def next_document(self):
        if self.controller.has_more_documents():
            self.controller.next_document()
            self.reload()
        else:
            self.open_file_dialog()

    def next_field(self):
        self.controller.next_field()
        self.reload()

    def on_enter_key_used(self):
        text = self.index_widget.index_text.toPlainText()
        if '\n' not in text and '\t' not in text:
            return
        text = (text.replace('\n', '')
                .replace('\t', '')
                .strip())
        self.controller.current_view.text = text
        self.controller.save_index_values()
        self.next_field()

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
                self,
                'Open EXPORT.TXT or select a PDF',
                common.pv_export_folder,
                'EXPORT.TXT (*.txt);; Single PDF (*.pdf)',
        )
        if file_name:
            self.controller.load_index_file(file_name)
            self.reload()
