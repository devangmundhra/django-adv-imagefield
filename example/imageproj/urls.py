from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from test_app.views import TestCreate

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'imageproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', TestCreate.as_view(), name='test_create'),
    url(r'^api/', include('media_field.api')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
