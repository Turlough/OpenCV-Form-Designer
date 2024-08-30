import sys
from glob import glob

from PyQt6.QtWidgets import QApplication

from design_controller import DesignController
from src.views.designer.page_design_view import PageDesignView


path = r"C:\_PV\forms"
scale = 0.29


def launch(folder):
    files = glob(f'{folder}\\*.tif')

    app = QApplication(sys.argv)
    controller = DesignController(files, scale)
    viewer = PageDesignView(controller)
    viewer.init_ui()
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    launch(path)
