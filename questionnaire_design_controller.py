from glob import glob
from queue import Queue

from page_design_controller import PageController


class QuestionnaireController:
    template_folder: str
    tiffs: Queue[str]
    current_controller: PageController

    def __init__(self, template_folder):
        self.template_folder = template_folder
        files = glob(f'{template_folder}\\*.tif')
        for f in files:
            self.tiffs.put(f)

