from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen

from src.models.other_fields import RadioGroup
from src.tools import colors
from src.views.designer.base_design_view import BaseDesignView
from src.views.designer.radio_button_design_view import RadioButtonDesignView


class RadioGroupDesignView(BaseDesignView):
    model: RadioGroup
    pen = QPen(colors.radio, 2)
    button_views: list[RadioButtonDesignView] = list()

    def __init__(self, model, scale, callback):
        super().__init__(model, scale, callback)
        self.button_views = list()
        rg = self.model.rectangle
        rg.x1, rg.y1 = rg.x2, rg.y2
        rg.x2 = rg.y2 = 0

        for b in self.model.buttons:
            rb = b.rectangle
            rg.x1 = min(rg.x1, rb.x1 - 2)
            rg.y1 = min(rg.y1, rb.y1 - 2)
            rg.x2 = max(rg.x2, rb.x2 + 4)
            rg.y2 = max(rg.y2, rb.y2 + 4)
            view = RadioButtonDesignView(b, self.scale, callback)
            self.button_views.append(view)
        super().__init__(model, scale, callback)

    def draw(self, painter):
        self.draw_rectangle(painter)
        self.draw_text(painter)
        for b in self.button_views:
            b.draw(painter)

    def draw_text(self, painter):
        x, y = self.rectangle.x(), self.rectangle.y()
        painter.drawText(x, y, self.model.name)
