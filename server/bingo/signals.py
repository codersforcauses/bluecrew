from .models import TileInteraction
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

# modified from https://stackoverflow.com/a/16041527


@receiver(post_delete, sender=TileInteraction)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `TileInteraction` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=TileInteraction)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `TileInteraction` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = TileInteraction.objects.get(pk=instance.pk).image
    except TileInteraction.DoesNotExist:
        return False

    new_image = instance.image
    if old_image and not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
