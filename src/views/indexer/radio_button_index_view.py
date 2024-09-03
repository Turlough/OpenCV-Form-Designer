from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from src.models.indexer.radio_group_response import RadioButtonResponse
from src.views.designer.global_functions import center_right
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButtonResponse
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)

    def __init__(self, model, scale):
        super().__init__(model, scale)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        tick_mark = '\u2714' if self.model.ticked else ''

        painter.drawText(x, y, tick_mark)

    def on_click(self, painter):
        self.model.tick()


