from PyQt6.QtGui import QFont, QPen

from src.models.other_fields import RadioButton
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButton
    scale: float
    pen = QPen(colors.radio, 2)

    def __init__(self, model, text, scale, on_item_indexed, group):
        super().__init__(model, text, scale, on_item_indexed, None)
        self.group = group

    def draw_text(self, painter):
        self.pen = QPen(colors.index, 2)
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        desc = self.model.name
        # desc = desc[:3] if len(desc) > 3 else desc
        tick_mark = '\u2714 ' + desc if self.ticked else ''

        painter.drawText(x, y, tick_mark)





