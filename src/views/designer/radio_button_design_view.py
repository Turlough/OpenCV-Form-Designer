from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import RadioButton
from src.views.designer.base_design_view import BaseDesignView


class RadioButtonDesignView(BaseDesignView):
    model: RadioButton
    pen = QPen(Qt.GlobalColor.darkYellow, 2)