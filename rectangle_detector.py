import sys

from PyQt6.QtWidgets import QApplication

from image_viewer import ImageViewer

path = r"C:\_PV\forms\SKM_C250i24081613480.tif"


def launch(image_path):
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.init_ui(image_path)
    viewer.showMaximized()

    app.exec()


if __name__ == '__main__':
    try:
        launch(path)
    except Exception as e:
        print(str(e))
        input('Fix the problem. Then press enter to exit. Then try relaunching the application')