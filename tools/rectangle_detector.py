import sys

from PyQt6.QtWidgets import QApplication

from controller import Controller
from views.page_view import PageView

path = r"C:\_PV\forms\SKM_C250i2408161348004.tif"
scale = 0.29


def launch(image_path):
    app = QApplication(sys.argv)
    controller = Controller(path, scale)
    viewer = PageView(controller)
    viewer.init_ui(image_path)
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(path)
