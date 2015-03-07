from django.contrib import admin
from .models import TestModel
from media_field.db import MediaField
from media_field.forms import MediaFieldWidget


class TestModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        MediaField: {'widget': MediaFieldWidget},
    }

admin.site.register(TestModel, TestModelAdmin)
