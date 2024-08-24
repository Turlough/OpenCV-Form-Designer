from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen

from models.answer_box import AnswerBox, BoxType


def color_for_answer(answer: AnswerBox):
    match answer.type:
        case BoxType.TICK:
            return Qt.GlobalColor.blue
        case BoxType.NUMBER:
            return Qt.GlobalColor.green
        case BoxType.TEXT:
            return Qt.GlobalColor.green

    return Qt.GlobalColor.red


def draw(answer: AnswerBox, painter, scale):
    pen = QPen(color_for_answer(answer), 2)
    painter.setPen(pen)
    ((x1, y1), (x2, y2)) = answer.rectangle.coordinates(scale=scale)
    rect = QRect(x1, y1, x2 - x1, y2 - y1)
    painter.drawRect(rect)
    painter.setFont(QFont("Arial", 6))
    # Calculate the height of the text
    font_metrics = painter.fontMetrics()
    text_height = font_metrics.height()
    text_start_y = rect.top() + (rect.height() - text_height) // 2 + text_height
    # Draw the text inside the rectangle
    painter.drawText(x2 + 5, text_start_y, answer.name)
