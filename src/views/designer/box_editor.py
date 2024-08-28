from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QComboBox, QDialogButtonBox, QLabel
)

from src.models.designer.answer_box import BoxType, AnswerBox


class BoxEditor(QDialog):
    def __init__(self, box: AnswerBox, parent=None):
        super(BoxEditor, self).__init__(parent)

        # Set up layout
        self.layout = QVBoxLayout(self)

        # Add a label and text coordinates
        self.label = QLabel(f'Enter new name for coordinates "{box.name}"')
        self.layout.addWidget(self.label)
        self.large_text_area = QLineEdit(self)
        self.layout.addWidget(self.large_text_area)

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
        return self.large_text_area.text()

    def get_type(self):
        return BoxType[self.comboBox.currentText()]
