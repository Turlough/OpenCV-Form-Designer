from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QFont, QPen

from src.models.other_fields import RadioButton
from src.tools import colors
from src.tools.global_functions import center_right
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButton
    scale: float
    pen = QPen(colors.radio, 1, Qt.PenStyle.DotLine)

    def __init__(self, model, text, scale, on_item_indexed, group):
        super().__init__(model, text, scale, on_item_indexed, None)
        self.group = group

    def draw_text(self, painter):
        self.text = self.model.name if self.ticked else ''
        if self.ticked:
            super().draw_text(painter)

    def on_click(self, painter, location):
        self.ticked = not self.ticked
        self.draw(painter)
