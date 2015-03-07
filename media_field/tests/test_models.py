from django.test import TestCase
from .. import models
from .. import forms


class TestMediaModelField(TestCase):
    def test_media_field_inherits_from_image_field(self):
        """MediaField should inherit from standard ImageField.
        """
        from django.db.models import ImageField
        self.assertIn(ImageField, models.MediaField.__bases__)

    def test_media_field_referres_the_correct_form_field(self):
        """MediaField of a model should point to MediaField for forms. That
        will be used while utilizing ModelForms.
        """
        media_field = models.MediaField()
        self.assertTrue(isinstance(media_field.formfield(), forms.MediaField))
