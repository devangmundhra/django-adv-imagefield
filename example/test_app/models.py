from django.db import models
from media_field.db import MediaField


class TestModel(models.Model):
    name = models.CharField(max_length=255)
    image = MediaField(blank=True, null=True, max_length=255)

    def __unicode__(self):
        return self.name


# Receive the pre_delete signal and delete the file associated with the model
# instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


@receiver(pre_delete, sender=TestModel)
def test_model_delete(sender, instance, **kwargs):
    # Pass false so ModelField doesn't save the model.
    instance.image.delete(False)
