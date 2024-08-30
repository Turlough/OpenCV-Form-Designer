from src.models.designer.answer_box import AnswerBox, RadioButton, RadioGroup, TickBox
from src.views.designer.radio_button_design_view import RadioButtonDesignView
from src.views.designer.radio_group_design_view import RadioGroupDesignView
from src.views.designer.text_design_view import TextDesignView


class ViewFactory:
    def __init__(self):
        # Map model classes to their corresponding view classes
        self._mapping = {
            AnswerBox: TextDesignView,
            TickBox: TextDesignView,
            RadioButton: RadioButtonDesignView,
            RadioGroup: RadioGroupDesignView
        }

    def create_view(self, model, scale):
        model_class = model.__class__  # Get the class of the model instance
        view_class = self._mapping.get(model_class)
        if view_class is None:
            raise ValueError(f"No view found for model class {model_class}")
        return view_class(model, scale)  # Create and return the view instance
