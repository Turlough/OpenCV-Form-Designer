from src.models.designer.answer_box import AnswerBox, RadioButton, RadioGroup, TickBox
from src.models.indexer.radio_group_response import RadioButtonResponse, RadioGroupResponse
from src.models.indexer.response_base import TextIndexResponse, TickBoxResponse
from src.views.indexer.radio_button_index_view import RadioButtonIndexView
from src.views.indexer.radio_group_index_view import RadioGroupIndexView
from src.views.indexer.text_index_view import TextIndexView
from src.views.indexer.tick_box_index_view import TickBoxIndexView


class IndexViewFactory:
    def __init__(self):
        # Map model classes to their corresponding view classes
        self._mapping = {
            AnswerBox: (TextIndexResponse, TextIndexView),
            TickBox: (TickBoxResponse, TickBoxIndexView),
            RadioButton: (RadioButtonResponse, RadioButtonIndexView),
            RadioGroup: (RadioGroupResponse, RadioGroupIndexView)
        }

    def create_view(self, model, scale, editor_callback=None):
        model_class = model.__class__  # Get the class of the model instance
        (response_class, view_class) = self._mapping.get(model_class)

        if view_class is None:
            raise ValueError(f"No view found for model class {model_class}")

        index_value = '?' # TODO: Read this from an index row
        response = response_class(model, index_value)

        return view_class(response, scale, editor_callback)

