from glob import glob


class TemplateManager:

    def __init__(self, template_folder):
        self.images = glob(f'{template_folder}\\*.tif')

    def get_template(self, page_no: int):
        image = self.images[page_no]
        json = image.replace('.tif', '.json')
        return json, image
