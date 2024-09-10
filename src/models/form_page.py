import os.path

from src.models.multi_choice_field import MultiChoice
from src.models.rectangle import Rectangle
from src.models.other_fields import BaseField


class FormPage(BaseField):
    image = None
    image_path: str
    json_path: str
    csv_path: str
    answers: list[BaseField]
    groups: list[MultiChoice]

    def __init__(self, path: str):
        self.name = 'Form Page'
        self.rectangle = Rectangle().from_corners(0, 0, 0, 0)
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.csv_path = path.replace('.tif', '.csv')
        self.groups = list()
        self.answers = list()

    def sort_by_csv(self):
        if not os.path.exists(self.csv_path):
            return
        # build a dictionary of names
        answer_dict = dict()
        ordered_list = list()
        for a in self.answers:
            answer_dict[a.name] = a
        # load the list of names sequentially, and for each name, append the corresponding answer to the ordered list
        with open(self.csv_path, 'r') as file:
            counter = 1
            while line := file.readline():
                cols = line.split(',')
                name = cols[0]
                ans = answer_dict[name]
                ans.in_seq = counter
                ans.out_seq = counter
                counter += 1
                ordered_list.append(ans)

        self.answers = ordered_list

