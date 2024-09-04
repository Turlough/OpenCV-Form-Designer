from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout

from src.models.designer.answer_base import AnswerBase
from src.models.designer.answer_box import NumberBox, RadioButton, TextBox, TickBox


class TypeChangeDialog(QDialog):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.return_value = AnswerBase.__class__
        # Remove the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Layout and widgets
        self.setLayout(QVBoxLayout())
        self.add_button('TickBox', TickBox)
        self.add_button('TextBox', TextBox)
        self.add_button('NumberBox', NumberBox)
        self.add_button('RadioButton', RadioButton)

    def add_button(self, name, new_model):
        btn = QPushButton(self)
        btn.setText(name)
        btn.clicked.connect(lambda: self.clicked(new_model))
        self.layout().addWidget(btn)
        return btn

    def clicked(self, new_model):
        self.return_value = new_model
        if self.callback:
            self.callback(new_model)
        self.accept()
