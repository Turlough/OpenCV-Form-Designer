from models.rectangle import Rectangle
from models.answer_box import AnswerBase, AnswerBox, GroupOfAnswers


class FormPage(AnswerBase):
    image = None
    image_path: str
    json_path: str
    answers: list[AnswerBox]
    groups: list[GroupOfAnswers]

    def __init__(self, path: str):
        self.name = 'Form Page'
        self.rectangle = Rectangle().from_corners(0, 0, 0, 0)
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.groups = list()
        self.answers = list()
