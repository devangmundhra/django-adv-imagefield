from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^media-field/images/$', views.url_image_list, name='media_field_api')
)
