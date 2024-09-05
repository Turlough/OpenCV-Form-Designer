from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from src.models.indexer.response_base import TickBoxResponse
from src.views.designer.global_functions import center_right
from src.views.indexer.base_index_view import BaseIndexView


class TickBoxIndexView(BaseIndexView):
    model: TickBoxResponse
    scale: float
    pen = QPen(Qt.GlobalColor.blue, 2)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 8))
        m = painter.fontMetrics()
        text_height = m.height()
        x, y = center_right(self.rectangle, text_height)
        desc = self.model.question.name
        desc = desc[:3] if len(desc) > 3 else desc
        tick_mark = '\u2714 ' + desc if self.model.ticked else ''

        painter.drawText(x, y, tick_mark)

    def on_click(self, painter, location):
        self.model.tick()
        self.draw(painter)
