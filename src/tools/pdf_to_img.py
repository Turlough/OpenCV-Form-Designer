from pdf2image import convert_from_path
import numpy as np

# Path to your Poppler installation (for Windows, point to the "bin" folder)
poppler_path = r"C:\Users\tcowman\py\rectangle_detector\poppler-24.07.0\Library\bin"


def get_page(path, page):
    pages = convert_from_path(path, poppler_path=poppler_path, dpi=300)
    return np.array(pages[page + 3])
