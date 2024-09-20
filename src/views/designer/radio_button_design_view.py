from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.other_fields import RadioButton
from src.tools import colors
from src.views.designer.base_design_view import BaseDesignView


class RadioButtonDesignView(BaseDesignView):
    model: RadioButton
    pen = QPen(colors.radio, 2, Qt.PenStyle.DotLine)
