from enum import Enum

from PyQt6.QtWidgets import QComboBox, QDialog, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton, \
    QDialogButtonBox
from PyQt6.QtCore import pyqtSlot


class ModelEditor(QDialog):
    def __init__(self, obj, callback=None, parent=None):

        super().__init__(parent)
        self.callback = callback
        self.setWindowTitle("Edit Object")

        self.obj = obj
        self.fields = {}

        layout = QVBoxLayout(self)

        # Create a form layout
        form_layout = QFormLayout()

        # Dynamically generate fields based on the object's attributes
        for attr_name, attr_value in vars(self.obj).items():
            if isinstance(attr_value, (str, int, float)):
                # Handle primitive types with QLineEdit
                line_edit = QLineEdit(self)
                line_edit.setText(str(attr_value))
                self.fields[attr_name] = line_edit
                form_layout.addRow(attr_name, line_edit)
            elif isinstance(attr_value, Enum):
                # Handle enum types with QComboBox
                combo_box = QComboBox(self)
                for enum_item in type(attr_value):
                    combo_box.addItem(enum_item.name)
                combo_box.setCurrentText(attr_value.name)
                self.fields[attr_name] = combo_box
                form_layout.addRow(attr_name, combo_box)
            elif isinstance(attr_value, object):
                # Handle nested objects with a button to open a new dialog
                edit_button = QPushButton(f"Edit {attr_name}", self)
                edit_button.clicked.connect(
                    lambda checked, name=attr_name, value=attr_value: self.edit_sub_object(name, value))
                form_layout.addRow(QLabel(attr_name), edit_button)

        layout.addLayout(form_layout)

        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        # Update the object's attributes with the values from the form
        for attr_name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text()
                if value.isdigit():
                    value = int(value)
                setattr(self.obj, attr_name, value)
            elif isinstance(widget, QComboBox):
                value = widget.currentText()
                enum_type = type(getattr(self.obj, attr_name))
                # Correctly map the selected string back to the enum
                for enum_member in enum_type:
                    if enum_member.name == value:
                        setattr(self.obj, attr_name, enum_member)
                        break

        if self.callback:
            self.callback()
        super().accept()

    def edit_sub_object(self, attr_name, sub_obj):
        # Create a sub-dialog for the nested object
        sub_dialog = ModelEditor(sub_obj, self)
        if sub_dialog.exec():
            setattr(self.obj, attr_name, sub_obj)
