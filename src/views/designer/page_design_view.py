import logging

from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QHBoxLayout, QInputDialog, QMainWindow, QPushButton, \
    QWidget, \
    QVBoxLayout, QTextEdit, \
    QScrollArea
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QFont

from src.design_controller import DesignController, EditMode

from src.views.designer.page_design_painter import PageDesignPainter

logging.basicConfig(format='%(levelname)s:  %(message)s', level=logging.ERROR)


class PageDesignView(QWidget):
    controller: DesignController
    edit: QTextEdit
    scroll_area: QScrollArea
    picture: PageDesignPainter

    def __init__(self, controller: DesignController):
        self.controller = controller
        self.scroll_area = QScrollArea()
        self.edit = QTextEdit()
        self.picture = PageDesignPainter(on_release=self.on_rectangle_drawn, controller=controller)
        super().__init__()

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

        radio_group_button = QPushButton()
        radio_group_button.setText("Create Radio Groups")
        radio_group_button.clicked.connect(lambda: self.set_mode(EditMode.RADIO_GROUP))

        new_box_button = QPushButton()
        new_box_button.setText("Draw new Fields")
        new_box_button.clicked.connect(lambda: self.set_mode(EditMode.CREATE_FIELD))

        relabel_button = QPushButton()
        relabel_button.setText('Edit Fields')
        relabel_button.clicked.connect(lambda: self.set_mode(EditMode.EDIT_FIELD))

        save_button = QPushButton()
        save_button.setText('Save and Reload')
        save_button.clicked.connect(self.save_and_reload)

        next_button = QPushButton()
        next_button.setText('Next page')
        next_button.clicked.connect(self.next_page)

        image_button_layout.addWidget(detect_button)
        image_button_layout.addWidget(new_box_button)
        image_button_layout.addWidget(radio_group_button)
        image_button_layout.addWidget(relabel_button)
        image_button_layout.addWidget(save_button)
        image_button_layout.addWidget(next_button)

        # Image area bottom left
        self.add_scroll_area_for_image(left_layout)

        # right hand side
        right_layout.addWidget(self.edit)
        font = QFont('Courier', 12)
        self.edit.setFont(font)

        self.setLayout(main_layout)

        image = self.controller.get_image()
        self.display(image)
        self.update_large_text_area()

    def update_large_text_area(self):
        self.edit.setText(self.controller.tabulate_view_models())

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

        self.reload()

    def on_rectangle_drawn(self, rect: QRect):
        match self.controller.edit_mode:
            case EditMode.EDIT_FIELD:
                self.edit_field(rect)
            case EditMode.CREATE_FIELD:
                self.create_field(rect)
            case EditMode.RADIO_GROUP:
                self.new_radio_group(rect)
        self.reload()

    def new_radio_group(self, rect: QRect):
        name, ok = QInputDialog.getText(self, 'Group Name', 'Type a name for this group')
        if not ok or not name:
            return

        x1, y1 = rect.topLeft().x(), rect.topLeft().y()
        x2, y2 = rect.bottomRight().x(), rect.bottomRight().y()

        self.controller.on_radio_group_drawn(name, x1, y1, x2, y2)
        self.update_large_text_area()

    def edit_field(self, rect: QRect):
        x, y = rect.topLeft().x(), rect.topLeft().y()
        view = self.controller.locate_surrounding_box(x + 1, y + 1)
        if not view:
            return
        view.on_click()
        self.save_and_reload()

    def create_field(self, rect):
        self.controller.create_field(rect)
        self.save_and_reload()
        self.edit_field(rect)

    def save_and_reload(self):
        self.controller.save_to_json()
        self.controller.load_from_json()
        self.reload()

    def detect_rectangles(self):
        self.set_mode(EditMode.NONE)
        self.controller.detect_rectangles()
        self.reload()

    def reload(self):
        self.update_large_text_area()
        self.picture.page = self.controller.page
        self.picture.draw_fields()
        # self.picture.draw_groups()

    def set_mode(self, mode: EditMode):
        self.controller.set_mode(mode)
        self.picture.mode = mode

    def next_page(self):
        self.controller.next()
        image = self.controller.get_image()
        self.picture.page = self.controller.page
        self.display(image)

