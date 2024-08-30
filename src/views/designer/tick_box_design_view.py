from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import TickBox
from src.views.designer.base_design_view import BaseDesignView


class TickBoxDesignView(BaseDesignView):
    model: TickBox
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)
