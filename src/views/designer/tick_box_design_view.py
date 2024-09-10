from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.other_fields import TickBox
from src.tools import colors
from src.views.designer.base_design_view import BaseDesignView


class TickBoxDesignView(BaseDesignView):
    model: TickBox
    scale: float
    pen = QPen(colors.tick, 2)
