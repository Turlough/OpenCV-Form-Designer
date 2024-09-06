from typing import Callable

from src.models.designer.answer_box import AnswerBox, NumberBox, RadioButton, TextBox, TickBox
from src.views.indexer.radio_button_index_view import RadioButtonIndexView
from src.views.indexer.text_index_view import TextIndexView
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class IndexViewFactory:
    def __init__(self, scale, on_index_completed: Callable):
        self.scale = scale
        self.on_index_completed = on_index_completed
        # Map model classes to their corresponding view classes
        self._mapping = {
            AnswerBox  : TextIndexView,
            TextBox    : TextIndexView,
            NumberBox  : TextIndexView,
            TickBox    : TickBoxIndexView,
        }

    def create_view(self, model, text):
        view_class = self._get_view_for_model(model)
        return view_class(model, text, self.scale, self.on_index_completed)

    def create_button_for_group(self, model: RadioButton, text, group):
        return RadioButtonIndexView(model, text, self.scale, self.on_index_completed, group)

    def _get_view_for_model(self, model):
        model_class = model.__class__  # Get the class of the model instance
        (view_class) = self._mapping.get(model_class)
        if view_class is None:
            raise ValueError(f"No view found for model class {model_class}")
        return view_class

