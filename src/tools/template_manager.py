from glob import glob


class TemplateManager:

    def __init__(self, template_folder):
        self.images = glob(f'{template_folder}\\*.tif')
        self.images = glob(f'{template_folder}\\*.jpg')
        self.images.sort()
        self.csvs = glob(f'{template_folder}\\*.csv')

    def get_template(self, page_no: int):
        image = self.images[page_no]
        json = image.replace('.tif', '.json')
        json = image.replace('.jpg', '.json')
        return json, image

    def get_field_counts(self):
        result = list()
        result.append(0)
        total = 0
        for path in self.csvs:
            num_lines = sum(1 for _ in open(path))
            total += num_lines
            result.append(total)
        return result

