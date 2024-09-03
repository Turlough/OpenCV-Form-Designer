from dataclasses import dataclass

from src.models.designer.answer_box import RadioButton, RadioGroup
from src.models.indexer.response_base import ResponseBase, TickBoxResponse


class RadioButtonResponse(TickBoxResponse):
    question: RadioButton

    def __init__(self, question, text, group):
        super().__init__(question, text)
        self.response_group = group

    def tick(self):
        self.ticked = not self.ticked
        self.text = self.question.name if self.ticked else ''
        self.response_group.notify_ticked(self)


class RadioGroupResponse(ResponseBase):
    question: RadioGroup
    button_responses: list[RadioButtonResponse]

    def __init__(self, question, text):
        super().__init__(question, text)
        self.button_responses = list()
        for rb in self.question.buttons:
            r = RadioButtonResponse(rb, rb.name, self)
            self.button_responses.append(r)

    def notify_ticked(self, button: RadioButtonResponse):
        for b in self.button_responses:
            if b is not button:
                b.ticked = False
                b.text = ''
        self.text = button.question.name




