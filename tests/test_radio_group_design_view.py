from unittest import TestCase

from src.models.other_fields import RadioButton, RadioGroup
from src.models.rectangle import Rectangle
from src.views.designer.design_view_factory import DesignViewFactory


class TestRadioGroupDesignView(TestCase):

    def test_minimum_box(self):
        r0 = Rectangle().from_corners(0, 0, 6, 6)
        g0 = RadioGroup('g0', r0)
        r1 = Rectangle().from_corners(1, 1, 2, 2)
        b1 = RadioButton('b1', r1, g0)
        r2 = Rectangle().from_corners(1, 3, 2, 4)
        b2 = RadioButton('b1', r2, g0)
        g0.buttons = [b1, b2]

        factory = DesignViewFactory()
        gv = factory.create_view(g0, 1, None)

        r = gv.model.rectangle
        self.assertEqual(r0.x1, r.x1)
        self.assertEqual(r0.y1, r.y1)
        self.assertEqual(r1.x2, r.x2)
        self.assertEqual(r1.y2, r.y2)
