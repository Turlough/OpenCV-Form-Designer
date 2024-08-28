import logging

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QApplication, QDialog, QHBoxLayout, QInputDialog, QMainWindow, QPushButton, \
    QWidget, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QCursor, QPixmap, QImage
from PyQt6.QtGui import QFont

from index_controller import IndexController
from models.answer_box import AnswerBox

from views.generic_model_editor import ModelEditor
from views.image_label import ImageLabel
from views.indexer.index_label import IndexLabel

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class IndexView(QWidget):
    controller: IndexController
    edit: QTextEdit
    scroll_area: QScrollArea
    picture: IndexLabel

    def __init__(self, controller: IndexController):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.edit = QTextEdit()
        self.picture = IndexLabel(controller=controller)
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

        detect_button = QPushButton()
        detect_button.setText("Locate Rectangles")
        detect_button.clicked.connect(self.detect_rectangles)

        box_group_button = QPushButton()
        box_group_button.setText("Create Groups")
        box_group_button.clicked.connect(lambda: self.set_mode(EditMode.BOX_GROUP))

        new_box_button = QPushButton()
        new_box_button.setText("Create Answer Boxes")
        new_box_button.clicked.connect(lambda: self.set_mode(EditMode.CREATE_BOX))

        relabel_button = QPushButton()
        relabel_button.setText('Edit Answer boxes')
        relabel_button.clicked.connect(lambda: self.set_mode(EditMode.BOX_EDIT))

        save_button = QPushButton()
        save_button.setText('Save and Reload')
        save_button.clicked.connect(self.save_and_reload)

        image_button_layout.addWidget(detect_button)
        image_button_layout.addWidget(new_box_button)
        image_button_layout.addWidget(box_group_button)
        image_button_layout.addWidget(relabel_button)
        image_button_layout.addWidget(save_button)

        # Image area bottom left
        self.add_scroll_area_for_image(left_layout)

        bottom_layout = QHBoxLayout()
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

    def new_group_box(self, rect: QRect):
        name, ok = QInputDialog.getText(self, 'Group Name', 'Type a name for this group')
        if not ok or not name:
            return

        x1, y1 = rect.topLeft().x(), rect.topLeft().y()
        x2, y2 = rect.bottomRight().x(), rect.bottomRight().y()

        self.controller.on_group_box_drawn(name, x1, y1, x2, y2)
        self.show_json()

    def edit_answer(self, rect: QRect):
        x, y = rect.topLeft().x(), rect.topLeft().y()
        box = self.controller.locate_surrounding_box(x + 1, y + 1)
        if not box:
            return
        mouse_pos = QCursor.pos()
        editor = ModelEditor(box, callback=self.save_and_reload)
        editor.move(mouse_pos)
        editor.exec()

    def create_answer(self, rect):
        self.controller.create_answer(rect)
        self.save_and_reload()
        self.edit_answer(rect)

    def save_and_reload(self):
        self.controller.save_to_json()
        self.controller.load_from_json()
        self.reload()

    def detect_rectangles(self):
        self.set_mode(EditMode.NONE)
        self.controller.detect_rectangles()
        self.reload()

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

