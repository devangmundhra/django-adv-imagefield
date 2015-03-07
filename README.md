# django-adv-imagefield
Advanced ImageField for Django that provides widget to search Flickr and Google Images

django-adv-imagefield allows you to add an ImageField and provides a widget that can be used to search for images in admin itself.

**To install ``django-adv-image-field``**
1. ``pip install django-adv-imagefield``
2. In settings.py add: ``media-field`` in ``INSTALLED_APPS``
3. In settings.py set: FLICKR_API_KEY, GOOGLE_API_KEY and GOOGLE_SENGINE_ID
4. In your root `url.py` add one more url pattern: ``url(r'^api/', include('media_field.api')),``
5. In your `models.py` import and add to your model `MediaField`
````
    from django.db import models
    from media_field.db import MediaField

    class TestModel(models.Model):
        name = models.CharField(max_length=255)
        image = MediaField(blank=True)

This will allow using ordinary ModelForm.
````

6. If you want using `MediaField` in django-admin, then in your app's admin.py import `MediaFieldWidget` and specify it for your `ModelAdmin`

````
    from django.contrib import admin
    from .models import TestModel
    from media_field.db import MediaField
    from media_field.forms import MediaFieldWidget

    class TestModelAdmin(admin.ModelAdmin):
        formfield_overrides = {
            MediaField: {'widget': MediaFieldWidget},
        }

    admin.site.register(TestModel, TestModelAdmin)
````

7. If you want to change default widget width (100%) and image width(30%), you may specify the width in your form field like this
````
    image = MediaField(blank=True, attrs={'width': '500px', 'image_width': '50%'})
````

**Installing and running test project**
1. Go to *example* directory
2. Run in the unpacked folder `pip install -r requirements.txt`
3. ``python manage.py makemigrations``
4. ``python manage.py migrate``
5. ``python manage.py createsuperuser``
6. ``python manage.py runserver``
7. Navigate to http://localhost:8000/admin , login and play with TestModel and MediaField.