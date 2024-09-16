import sys
from glob import glob

from PyQt6.QtWidgets import QApplication

from index_controller import IndexController
from src.views.indexer.page_index_view import PageIndexView


template_folder = r"C:\_PV\forms2"
scale = 0.3051
index_path = r"C:\_PV\IFAC\EXPORT\24151 1111101\EXPORT.TXT"


def launch(folder):
    app = QApplication(sys.argv)
    controller = IndexController(folder, scale)
    viewer = PageIndexView(controller)
    viewer.init_ui()
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(template_folder)
