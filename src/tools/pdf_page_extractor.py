from pdf2image import convert_from_path
import numpy as np

from src.tools import common


class PdfExtractor:

    def __init__(self, path):
        try:
            self.pages = convert_from_path(path, poppler_path=common.poppler_path, dpi=common.index_resolution)
        except Exception as ex:
            print(ex)

    def get_page(self, page):
        return np.array(self.pages[page + 3])
