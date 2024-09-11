from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import TextBox
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TextIndexView(BaseIndexView):
    model: TextBox
    pen = QPen(colors.text, 2)

    def draw_text(self, painter):
        painter.setPen(QPen(colors.index, 2))
        painter.setFont(QFont("Arial", 10))
        # Calculate the height of the text
        m = painter.fontMetrics()
        text_height = m.height()
        text_x, text_y = center_right(self.rectangle, text_height)
        painter.drawText(text_x, text_y, self.text)
