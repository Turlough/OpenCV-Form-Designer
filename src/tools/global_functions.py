from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from src.models.multi_choice_field import MultiChoice


def center_right(rect, text_height):
    return rect.right() + 5, rect.top() + (rect.height() - text_height) // 2 + text_height


