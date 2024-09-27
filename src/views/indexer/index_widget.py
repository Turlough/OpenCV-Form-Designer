from PyQt6.QtCore import QMetaObject
from PyQt6.QtGui import QFont, QImage, QPixmap, QTextCursor
from PyQt6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget
from src.views.indexer.text_index_view import LongTextIndexView


class IndexWidget(QWidget):
    """Thumbnail of current field with text box. For Indexing of text"""
    index_text: QTextEdit
    small_picture: QLabel
    connection: QMetaObject = None

    def __init__(self, parent, on_enter_key_used):
        super().__init__(parent)
        self.on_enter_key_used = on_enter_key_used

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.small_picture = QLabel()
        self.index_text = QTextEdit()
        self.index_text.textChanged.connect(on_enter_key_used)

        layout.addWidget(self.small_picture)
        layout.addWidget(self.index_text)

    def display(self, view, cropped):
        # Set the Pixmap
        h, w, ch = cropped.shape
        bytes_per_line = ch * w
        qt_image = QImage(cropped.data.tobytes(), w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pixmap = QPixmap(qt_image)
        self.small_picture.setPixmap(pixmap)
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


