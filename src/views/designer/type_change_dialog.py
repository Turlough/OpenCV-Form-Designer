from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout

from src.models.designer.answer_base import AnswerBase
from src.models.designer.answer_box import TickBox


class TypeChangeDialog(QDialog):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.return_value = AnswerBase.__class__
        # Remove the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Layout and widgets
        self.setLayout(QVBoxLayout())
        self.tick_box = self.add_button('TickBox', self.test_click)
        # self.tick_box.setText(text)
        self.layout().addWidget(self.tick_box)

    def add_button(self, name, on_click):
        btn = QPushButton(self)
        btn.setText(name)
        btn.clicked.connect(on_click)
        self.layout().addWidget(btn)
        return btn

    def test_click(self):
        self.return_value = TickBox
        if self.callback:
            self.callback(TickBox)
        self.accept()
