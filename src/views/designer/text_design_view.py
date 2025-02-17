from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.other_fields import LongTextBox, NumberBox, TextBox
from src.tools import colors
from src.views.designer.base_design_view import BaseDesignView


class TextDesignView(BaseDesignView):
    model: TextBox
    pen = QPen(colors.text, 2)


class NumberDesignView(TextDesignView):
    model: NumberBox
    pen = QPen(colors.number, 2, Qt.PenStyle.DotLine)


class LongTextDesignView(TextDesignView):
    model: LongTextBox
    pen = QPen(colors.text, 2, Qt.PenStyle.DotLine)
