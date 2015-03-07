from django.test import TestCase
from ..forms import MediaField, MediaFieldWidget


class TestMediaFormField(TestCase):
    def test_media_field_inherits_from_image_field(self):
        """MediaField should inherit from standard ImageField.
        """
        from django.forms import ImageField
        self.assertIn(ImageField, MediaField.__bases__)

    def test_media_field_should_have_correct_widget(self):
        """MediaField of a form should have MediaFieldWidget.
        """
        self.assertEqual(MediaField.widget, MediaFieldWidget)


class TestMediaFieldWidget(TestCase):
    def test_widget_renders_correct_string(self):
        """test_widget_renders_correct_string.
        """
        widget = MediaFieldWidget()
        self.assertEqual(widget.render('hello', 'world'), 'hello world!!!')
