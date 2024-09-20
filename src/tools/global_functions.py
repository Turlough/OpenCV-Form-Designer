from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QFont, QPen
from src.models.multi_choice_field import MultiChoice


def center_right(rect, h):
    return rect.right(), rect.top() + (rect.height() - h) // 2 + h


def center(rect, w, h):
    x = rect.left() + (rect.width() - w) // 2
    y = rect.top() + (rect.height() - h) // 2 + h
    return x, y


def center_left(rect, w, h):
    x = rect.left() - w
    y = rect.top() + (rect.height() - h) // 2 + h
    return x, y


