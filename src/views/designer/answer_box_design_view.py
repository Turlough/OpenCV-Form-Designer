from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPen

from src.models.designer.answer_box import AnswerBox
from src.views.designer.answer_box_painter import center_right
from src.views.designer.design_base_view import BaseDesignView


class AnswerBoxDesignView(BaseDesignView):
    model: AnswerBox
    pen = QPen(Qt.GlobalColor.red, 2)


