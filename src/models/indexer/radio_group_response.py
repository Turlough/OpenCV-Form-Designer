from dataclasses import dataclass

from src.models.designer.answer_box import RadioButton, RadioGroup
from src.models.indexer.response_base import ResponseBase, TickBoxResponse


class RadioButtonResponse(ResponseBase):
    question: RadioButton

    def __init__(self, question, text, group):
        super().__init__(question, text)
        self.response_group = group


class RadioGroupResponse(ResponseBase):
    question: RadioGroup
    button_responses: list[RadioButtonResponse]

    def __init__(self, question, text):
        super().__init__(question, text)
        self.button_responses = list()
        for rb in self.question.buttons:
            r = RadioButtonResponse(rb, rb.name, self)
            self.button_responses.append(r)

        for b in self.button_responses:
            b.ticked = False
            b.text = ''
            if b.question.name == text:
                b.ticked = True
                b.text = b.question.name
                self.text = text
