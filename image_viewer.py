import logging

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QInputDialog, QMainWindow, QPushButton, \
    QWidget, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QFont

from controller import Controller, EditMode
from views.box_editor import BoxEditor
from views.generic_model_editor import ModelEditor
from views.image_label import ImageLabel

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
        box_group_button = QPushButton()
        box_group_button.setText("Box Groups")
        box_group_button.clicked.connect(lambda: self.controller.set_mode(EditMode.BOX_GROUP))

        image_button_layout.addWidget(box_group_button)
        relabel_button = QPushButton()
        relabel_button.setText('Rename coordinates areas')
        image_button_layout.addWidget(relabel_button)
        relabel_button.clicked.connect(lambda: self.controller.set_mode(EditMode.BOX_EDIT))
        # Image area bottom left
        self.add_scroll_area_for_image(left_layout)
        # right hand side
        right_layout.addWidget(self.edit)
        font = QFont()
        font.setPointSize(20)
        self.edit.setFont(font)

        self.setLayout(main_layout)

        image = self.controller.get_image()
        self.display(image)

        self.load_json()

    def load_json(self):
        self.edit.setText(self.controller.get_page_json())

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
        match self.controller.edit_mode:
            case EditMode.BOX_GROUP:
                self.new_group_box(rect)
            case EditMode.BOX_EDIT:
                self.edit_box(rect)

    def new_group_box(self, rect: QRect):
        name, ok = QInputDialog.getText(self, 'Group Name', 'Type a name for this group')
        if not ok or not name:
            return

        x1, y1 = rect.topLeft().x(), rect.topLeft().y()
        x2, y2 = rect.bottomRight().x(), rect.bottomRight().y()

        self.controller.on_group_box_drawn(name, x1, y1, x2, y2)
        self.load_json()

    def edit_box(self, rect: QRect):
        x, y = rect.topLeft().x(), rect.topLeft().y()
        box = self.controller.locate_surrounding_box(x, y)
        if not box:
            return

        ModelEditor(box, callback=self.save_and_reload()).exec()

    def save_and_reload(self):
        self.controller.save_json()
        self.load_json()
