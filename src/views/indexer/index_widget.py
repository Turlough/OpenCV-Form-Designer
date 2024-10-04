
from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget

from src.views.indexer.image_label import ImageLabel
from src.views.indexer.text_index_view import LongTextIndexView


class IndexWidget(QWidget):
    """Thumbnail of current field with text box. For Indexing of text"""
    index_text: QTextEdit
    picture_label: ImageLabel
    connection: QMetaObject = None

    def __init__(self, parent, on_enter_key_used):
        super().__init__(parent)
        self.on_enter_key_used = on_enter_key_used

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.picture_label = ImageLabel()

        self.index_text = QTextEdit()
        self.index_text.textChanged.connect(on_enter_key_used)

        layout.addWidget(self.picture_label)
        layout.addWidget(self.index_text)

    def display(self, view, cropped):
        self.picture_label.load_cv_image(cropped)
        if isinstance(view, LongTextIndexView):
            self.show_long_text(view.text)
        else:
            self.show_short_text(view.text)

    def show_long_text(self, text):
        self.index_text.setFont(QFont('Arial', 10))
        self.index_text.setMaximumHeight(200)
        self.set_text(text)

    def show_short_text(self, text):
        self.index_text.setFont(QFont('Arial', 20))
        self.index_text.setMaximumHeight(50)
        self.set_text(text)

    def set_text(self, text):
        self.index_text.setText(text)
        cursor = self.index_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.index_text.setTextCursor(cursor)


