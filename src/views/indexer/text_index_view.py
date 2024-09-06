from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from PyQt6.QtWidgets import QDialog

from src.models.designer.answer_box import TextBox
from src.views.designer.global_functions import center_right
from src.views.indexer.index_value_dialog import IndexDialog
from src.views.indexer.base_index_view import BaseIndexView


class TextIndexView(BaseIndexView):
    model: TextBox
    pen = QPen(Qt.GlobalColor.darkGreen, 2)

    def on_click(self, painter, location):

        dialog = IndexDialog(self.text)
        x, y = self.rectangle.right() + 100, self.rectangle.bottom() + 30
        dialog.move(x, y)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.text = dialog.lineEdit.text()
            self.on_item_indexed()
        # self.on_item_indexed(self.model)
        self.draw(painter)

    def draw_text(self, painter):
        painter.setFont(QFont("Arial", 10))
        # Calculate the height of the text
        m = painter.fontMetrics()
        text_height = m.height()
        text_x, text_y = center_right(self.rectangle, text_height)
        painter.drawText(text_x, text_y, self.text[:5])
