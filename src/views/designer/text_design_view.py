from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import AnswerBox
from src.views.designer.base_design_view import BaseDesignView


class TextDesignView(BaseDesignView):
    model: AnswerBox
    pen = QPen(Qt.GlobalColor.red, 2)


