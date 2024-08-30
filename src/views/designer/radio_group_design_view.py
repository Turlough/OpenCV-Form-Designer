from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.designer.answer_box import RadioGroup
from src.views.designer.base_design_view import BaseDesignView
from src.views.designer.radio_button_design_view import RadioButtonDesignView


class RadioGroupDesignView(BaseDesignView):
    model: RadioGroup
    pen = QPen(Qt.GlobalColor.darkYellow, 2)
    button_views: list[RadioButtonDesignView] = list()

    def __init__(self, model, scale):
        super().__init__(model, scale)

        for b in self.model.buttons:
            view = RadioButtonDesignView(b, self.scale)
            self.button_views.append(view)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)
        for b in self.button_views:
            b.draw(painter)

    def draw_text(self, painter):
        x, y = self.rectangle.x(), self.rectangle.y()
        painter.drawText(x, y, self.model.name)
