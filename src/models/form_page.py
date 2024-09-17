import os.path

from src.models.multi_choice_field import MultiChoice
from src.models.rectangle import Rectangle
from src.models.other_fields import BaseField


class FormPage(BaseField):
    image = None
    image_path: str
    json_path: str
    csv_path: str
    fields: list[BaseField]
    groups: list[MultiChoice]

    def __init__(self, path: str):
        self.name = 'Form Page'
        self.rectangle = Rectangle().from_corners(0, 0, 0, 0)
        self._calculate_paths(path)
        self.groups = list()
        self.fields = list()

    def _calculate_paths(self, path):
        self.image_path = path
        self.json_path = path.replace('.jpg', '.json')
        self.json_path = self.json_path.replace('.tif', '.json')
        self.csv_path = path.replace('.jpg', '.csv')
        self.csv_path = self.csv_path.replace('.tif', '.csv')

    def sort_by_csv(self, image_path):
        self._calculate_paths(image_path)
        if not os.path.exists(self.csv_path):
            return
        # build a dictionary of names
        field_dict = dict()
        ordered_list = list()
        for f in self.fields:
            field_dict[f.name] = f
        # load the list of names sequentially, and for each name, append the corresponding answer to the ordered list
        with open(self.csv_path, 'r') as file:
            while line := file.readline():
                f = field_dict[str(line).strip()]
                ordered_list.append(f)

        self.fields = ordered_list

