import sys
from glob import glob

from PyQt6.QtWidgets import QApplication

from page_design_controller import PageController
from views.page_view import PageView


path = r"C:\_PV\forms"
scale = 0.29


def launch(folder):
    files = glob(f'{folder}\\*.tif')

    app = QApplication(sys.argv)
    controller = PageController(files, scale)
    viewer = PageView(controller)
    viewer.init_ui()
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(path)
