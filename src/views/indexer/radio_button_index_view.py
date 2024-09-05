from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from src.models.indexer.radio_group_response import RadioButtonResponse
from src.views.designer.global_functions import center_right
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class RadioButtonIndexView(TickBoxIndexView):
    model: RadioButtonResponse
    scale: float
    pen = QPen(Qt.GlobalColor.darkYellow, 2)

    def on_click(self, painter, location):
        self.model.tick()


