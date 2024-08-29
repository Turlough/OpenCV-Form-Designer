from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout


class IndexDialog(QDialog):
    def __init__(self, text: str, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        # Remove the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Layout and widgets
        self.setLayout(QVBoxLayout())
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setText(text)
        self.layout().addWidget(self.lineEdit)

        # Connect the Enter key press to accept the dialog
        self.lineEdit.returnPressed.connect(self.accept)

    def on_click(self):
        if self.callback:
            self.callback(self.lineEdit.text())
        self.accept()
