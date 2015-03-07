from django.forms import URLField
from django.forms.widgets import Widget
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.db.models.fields.files import ImageFieldFile
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse


widget_template = '''
<div {attrs} class="media_widget_wrapper" {width}>
    <div class="media_widget_row">
        <img id="media_widget_image" src="{value}" {image_width}/>
        <input id="media_widget_image_hidden" type="hidden" name="{name}">
        </input>
    </div>
    <br/>
    <div class="media_widget_row">
        <div class="media_widget_inputs" {image_width}>
            <input id="searchInput" placeholder="Enter Search Term" type="text">
            </input>
            <input id="searchButton" type="submit" value="Search">
            </input>
        </div>
        <br/>
    </div>
    <div class="media_widget_row" id="flickr_google_wrapper">
    </div>
    <br/>
    <div class="media_widget_row">
        <div class="media_widget_inputs" {image_width}>
            <input id="urlInput" placeholder="http://example.com" type="text">
            </input>
            <input id="urlButton" type="submit" value="Go">
            </input>
        </div>
    </div>
    <div class="media_widget_row" id="url_wrapper">
    </div>
</div>
<script type="text/javascript" charset="utf-8">
    var FLICKR_API_KEY = "{flickr_api}";
    var GOOGLE_API_KEY = "{google_api}";
    var GOOGLE_SENGINE_ID = "{google_sengine}";
    var MEDIA_FIELD_API = "{media_field_api}";
</script>'''


class MediaFieldWidget(Widget):
    class Media:
        css = {
            'all': ('/static/media_field/media_field.css',)
        }
        js = ('/static/media_field/mediaField.js',)

    def render(self, name, value, attrs=None):
        val = ''
        if type(value) is ImageFieldFile:
            val = value.url
        if not attrs:
            attrs = {}

        width_value = attrs.pop('width', None)
        width = 'style="width:{0}"'.format(width_value) if width_value else ''
        image_width_value = attrs.pop('image_width', None)
        image_width = 'style="width:{0}"'.format(image_width_value) \
            if width_value else ''
        attrs_string = flatatt(attrs)

        FLICKR_API_KEY = getattr(settings, 'FLICKR_API_KEY', None)
        GOOGLE_API_KEY = getattr(settings, 'GOOGLE_API_KEY', None)
        GOOGLE_SENGINE_ID = getattr(settings, 'GOOGLE_SENGINE_ID', None)
        MEDIA_FIELD_API = reverse('media_field_api')

        if not FLICKR_API_KEY or not GOOGLE_API_KEY or not GOOGLE_SENGINE_ID:
            raise ImproperlyConfigured('You need to provide FLICKR_API_KEY, \
                                       GOOGLE_API_KEY and GOOGLE_SENGINE_ID\
                                       in your settings.py')

        return format_html(widget_template,
                           attrs=unicode(attrs_string),
                           width=unicode(width),
                           image_width=unicode(image_width),
                           value=unicode(val),
                           name=unicode(name),
                           flickr_api=unicode(FLICKR_API_KEY),
                           google_api=unicode(GOOGLE_API_KEY),
                           google_sengine=unicode(GOOGLE_SENGINE_ID),
                           media_field_api=unicode(MEDIA_FIELD_API))


class MediaField(URLField):
    widget = MediaFieldWidget
