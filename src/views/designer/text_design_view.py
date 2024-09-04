from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import AnswerBox, TextBox
from src.views.designer.base_design_view import BaseDesignView


class TextDesignView(BaseDesignView):
    model: TextBox
    pen = QPen(Qt.GlobalColor.red, 2)
