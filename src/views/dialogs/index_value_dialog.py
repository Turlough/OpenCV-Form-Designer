from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
import pyperclip
from src.models.base_field import BaseField


class TextDialog(QDialog):
    model: BaseField

    def __init__(self, model: BaseField, parent=None, callback=None):
        super().__init__(parent)
        self.model = model
        self.callback = callback
        # Remove the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Layout and widgets
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.text_box = QLineEdit(self)
        s = pyperclip.paste()
        if s:
            self.text_box.setText(s)
        else:
            self.text_box.setText(model.name)
        self.text_box.selectAll()
        layout.addWidget(self.text_box)

        self.submit = QPushButton()
        self.submit.setText('Go')
        layout.addWidget(self.submit)

        # Connect the Enter key press to accept the dialog
        self.text_box.returnPressed.connect(self.on_return_pressed)
        self.submit.clicked.connect(self.on_return_pressed)

    def on_return_pressed(self):
        self.model.name = self.text_box.text()
        if self.callback:
            self.callback()
        self.accept()
