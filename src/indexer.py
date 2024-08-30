import sys
from glob import glob

from PyQt6.QtWidgets import QApplication

from index_controller import IndexController
from src.views.indexer.page_index_view import PageIndexView


path = r"C:\_PV\forms"
scale = 0.29


def launch(folder):
    files = glob(f'{folder}\\*.tif')

    app = QApplication(sys.argv)
    controller = IndexController(files, scale)
    viewer = PageIndexView(controller)
    viewer.init_ui()
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(path)
