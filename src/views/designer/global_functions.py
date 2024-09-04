from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from src.models.designer.group_of_answers import GroupOfAnswers


def center_right(rect, text_height):
    return rect.right() + 5, rect.top() + (rect.height() - text_height) // 2 + text_height


def draw_group(group: GroupOfAnswers, painter, scale):
    pen = QPen(Qt.GlobalColor.darkYellow, 2)
    painter.setPen(pen)
    ((x1, y1), (x2, y2)) = group.rectangle.coordinates(scale=scale)
    rect = QRect(x1, y1, x2 - x1, y2 - y1)
    painter.drawRect(rect)
    painter.setFont(QFont("Arial", 10))
    # Calculate the height of the text
    m = painter.fontMetrics()
    text_height = m.height()
    text_x = rect.left()
    text_y = rect.top() - 5
    # Draw the text inside the rectangle
    text = f'{group.name}'
    painter.drawText(text_x, text_y, text)
