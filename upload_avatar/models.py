# -*- coding: utf-8 -*-
import os

from django.db import models
from django.db.models.signals import post_delete


from .app_settings import UPLOAD_AVATAR_UPLOAD_ROOT


class UploadAvatarMixIn:
    """MUST define self.get_uid() method for using this mixin
    self.get_uid() return the current user's uid
    """
    def get_uploaded_image_name(self):
        try:
            return UploadedImage.objects.only('image').get(uid=self.get_uid())
        except UploadedImage.DoesNotExist:
            return None
        
    def get_uploaded_image_path(self):
        name = self.get_uploaded_image_name()
        if not name:
            return name
        
        full_path = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, name)
        if not os.path.exists(full_path):
            # delete from UploadedImage ??
            return None
        return full_path



class UploadedImage(models.Model):
    uid = models.IntegerField(unique=True)
    image = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def get_image_path(self):
        path = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, self.image)
        if not os.path.exists(path):
            return None
        return path


def _delete_avatar_on_disk(sender, instance, *args, **kwargs):
    path = instance.get_image_path()
    if path:
        try:
            os.unlink(path)
        except OSError:
            pass
    
    
post_delete.connect(_delete_avatar_on_disk, sender=UploadedImage)

