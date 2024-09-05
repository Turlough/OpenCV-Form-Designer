from pdf2image import convert_from_path
import numpy as np

# Path to your Poppler installation (for Windows, point to the "bin" folder)
poppler_path = r"C:\Users\tcowman\py\rectangle_detector\poppler-24.07.0\Library\bin"


class PdfExtractor:

    def __init__(self, path):
        self.pages = convert_from_path(path, poppler_path=poppler_path, dpi=300)

    def get_page(self, page):
        return np.array(self.pages[page + 3])
