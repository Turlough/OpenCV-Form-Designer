from src.models.other_fields import BaseField, LongTextBox, NumberBox, RadioButton, RadioGroup, TextBox, TickBox
from src.views.designer.base_design_view import BaseDesignView
from src.views.designer.radio_button_design_view import RadioButtonDesignView
from src.views.designer.radio_group_design_view import RadioGroupDesignView
from src.views.designer.text_design_view import LongTextDesignView, NumberDesignView, TextDesignView
from src.views.designer.tick_box_design_view import TickBoxDesignView


class DesignViewFactory:
    def __init__(self):
        # Map model classes to their corresponding view classes
        self._mapping = {
            BaseField: BaseDesignView,
            TickBox: TickBoxDesignView,
            TextBox: TextDesignView,
            NumberBox: NumberDesignView,
            RadioButton: RadioButtonDesignView,
            RadioGroup: RadioGroupDesignView,
            LongTextBox: LongTextDesignView
        }

    def create_view(self, model, scale, editor_callback):
        model_class = model.__class__  # Get the class of the model instance
        view_class = self._mapping.get(model_class)
        if view_class is None:
            raise ValueError(f"No view found for model class {model_class}")
        return view_class(model, scale, editor_callback)  # Create and return the view instance

