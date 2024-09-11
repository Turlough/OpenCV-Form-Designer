from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import NumberBox, TextBox
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView
from src.views.indexer.text_index_view import TextIndexView


class NumberIndexView(TextIndexView):
    model: NumberBox
    pen = QPen(colors.number, 2)
