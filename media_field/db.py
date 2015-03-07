from django.db.models import ImageField
from .forms import MediaField as MF
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import urllib2
from django.core.exceptions import SuspiciousFileOperation


class MediaField(ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': MF}
        defaults.update(kwargs)
        return super(ImageField, self).formfield(**defaults)

    def save_form_data(self, instance, data):
        # Important: None means "no change", other false value means "clear"
        # This subtle distinction (rather than a more explicit marker) is
        # needed because we need to consume values that are also sane for a
        # regular (non Model-) Form to find in its cleaned_data dictionary.
        # To default None for "no change" empty string '' also added, because
        # all changes to the field are made through input.hidden. The latter
        # is not initialized when the form is rendered for already existing
        # model.
        if data is not None and data is not u'':
            # This value will be converted to unicode and stored in the
            # database, so leaving False as-is is not acceptable.
            if not data:
                data = ''
            else:
                file_name = data.split('/')[-1]
                resource = urllib2.urlopen(data)
                if 'image' != resource.headers.getmaintype():
                    raise SuspiciousFileOperation('You are trying to download\
                                                  not image')
                f = ContentFile(resource.read())
                data = InMemoryUploadedFile(
                    f,
                    self.name,
                    file_name,
                    resource.headers.gettype(),
                    f.size,
                    resource.headers.getencoding()
                )
                self._committed = False

                # delete current file associated with the field
                field = getattr(instance, self.name, None)
                if field:
                    field.delete(False)
            setattr(instance, self.name, data)
