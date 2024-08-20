from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QDialogButtonBox, QLabel
)

from models.tickbox import BoxType, TickBox


class BoxEditor(QDialog):
    def __init__(self, box: TickBox, parent=None):
        super(BoxEditor, self).__init__(parent)

        # Set up layout
        self.layout = QVBoxLayout(self)

        # Add a label and text box
        self.label = QLabel(f'Enter new name for box "{box.name}"')
        self.layout.addWidget(self.label)
        self.textBox = QLineEdit(self)
        self.layout.addWidget(self.textBox)

        # Add a label and dropdown (combobox)
        self.enumLabel = QLabel("Select Box Type?")
        self.layout.addWidget(self.enumLabel)
        self.comboBox = QComboBox(self)
        self.layout.addWidget(self.comboBox)

        # Populate the dropdown with enum values
        for item in BoxType:
            self.comboBox.addItem(item.name, item.value)

        # Add standard buttons (OK and Cancel)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.buttonBox)

        # Connect the buttons to their respective slots
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_name(self):
        return self.textBox.text()

    def get_type(self):
        return BoxType[self.comboBox.currentText()]
