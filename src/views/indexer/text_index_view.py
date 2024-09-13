from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import TextBox
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TextIndexView(BaseIndexView):
    model: TextBox
    pen = QPen(colors.text, 2)