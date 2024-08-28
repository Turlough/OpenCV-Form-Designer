import json
from dataclasses import dataclass

from models.answer_base import AnswerBase, BoxType


@dataclass
class AnswerBox(AnswerBase):
    type: BoxType = BoxType.TICK

