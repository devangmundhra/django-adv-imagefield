from django.test import TestCase
from django.db.models import ImageField

from media_field.db import MediaField
from media_field import forms


class TestMediaModelField(TestCase):
    def test_media_field_inherits_from_image_field(self):
        """MediaField should inherit from standard ImageField.
        """
        self.assertIn(ImageField, MediaField.__bases__)

    def test_media_field_referres_the_correct_form_field(self):
        """MediaField of a model should point to MediaField for forms. That
        will be used while utilizing ModelForms.
        """
        media_field = MediaField()
        self.assertTrue(isinstance(media_field.formfield(), forms.MediaField))
