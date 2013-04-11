# -*- coding: utf-8 -*-
import os

from django.db import models
from django.db.models.signals import post_delete


from .app_settings import UPLOAD_AVATAR_UPLOAD_ROOT, UPLOAD_AVATAR_AVATAR_ROOT, UPLOAD_AVATAR_URL_PREFIX_CROPPED, UPLOAD_AVATAR_SAVE_FORMAT, UPLOAD_AVATAR_DEFAULT_SIZE


class UploadAvatarMixIn:
    """user MUST define self.get_uid(), and self.get_avatar_name() method for using this mixin
    self.get_uid() return the current user's uid,
    self.get_avatar_name() return avatar name
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
    
    
    def build_avatar_name(self, name, size):
        return '%s-%d.%s' % (name, size, UPLOAD_AVATAR_SAVE_FORMAT)
    
    def get_avatar_path(self, size=UPLOAD_AVATAR_DEFAULT_SIZE):
        full_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, self.get_avatar_name(size))
        if not os.path.exists(full_path):
            return None
        return full_path
    
    def get_avatar_url(self, size=UPLOAD_AVATAR_DEFAULT_SIZE):
        return UPLOAD_AVATAR_URL_PREFIX_CROPPED + self.get_avatar_name(size)
    



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

