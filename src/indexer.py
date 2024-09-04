import sys
from glob import glob

from PyQt6.QtWidgets import QApplication

from index_controller import IndexController
from src.views.indexer.page_index_view import PageIndexView


path = r"C:\_PV\forms"
scale = 0.29
index_path = r"C:\_PV\IFAC\EXPORT\24151 1111101\EXPORT.TXT"


def launch(folder, index_path):
    files = glob(f'{folder}\\*.tif')

    app = QApplication(sys.argv)
    controller = IndexController(files, scale, index_path)
    viewer = PageIndexView(controller)
    viewer.init_ui()
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(path, index_path)
