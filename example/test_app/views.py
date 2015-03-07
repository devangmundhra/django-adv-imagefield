from django.views.generic.edit import CreateView
from .models import TestModel


class TestCreate(CreateView):
    model = TestModel
    template_name = 'test_app/test.html'
