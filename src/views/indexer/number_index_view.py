from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import NumberBox
from src.tools import colors
from src.views.indexer.text_index_view import TextIndexView


class NumberIndexView(TextIndexView):
    model: NumberBox
    pen = QPen(colors.number, 2, Qt.PenStyle.DotLine)
