# -*- coding: utf-8 -*-

import os
import hashlib
import time
from functools import wraps

from PIL import Image

from django.http import HttpResponse
from django.utils.crypto import get_random_string

from .app_settings import (
    UPLOAD_AVATAR_TEST_FUNC as test_func,
    UPLOAD_AVATAR_GET_UID_FUNC as get_uid,
    UPLOAD_AVATAR_MAX_SIZE,
    UPLOAD_AVATAR_UPLOAD_ROOT,
    UPLOAD_AVATAR_AVATAR_ROOT,
    UPLOAD_AVATAR_URL_PREFIX_ORIGINAL,
    UPLOAD_AVATAR_RESIZE_SIZE,
    UPLOAD_AVATAR_SAVE_FORMAT,
    UPLOAD_AVATAR_SAVE_QUALITY,
    UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP,
)




from .signals import avatar_crop_done
from .models import UploadedImage


class UploadAvatarError(Exception):
    pass



def protected(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not test_func(request):
            print 'test failure'
            print request.user
            return HttpResponse(status=403)
        try:
            return func(request, *args, **kwargs)
        except UploadAvatarError as e:
            return HttpResponse(
                "<script>window.parent.upload_avatar_error('%s')</script>" % e
            )
    return deco


@protected
def upload_avatar(request):
    print request.user.username
    try:
        uploaded_file = request.FILES['uploadavatarfile']
    except KeyError:
        return HttpResponse(status=403)
    
    if uploaded_file.size > UPLOAD_AVATAR_MAX_SIZE:
        return HttpResponse("File too large", status=403)
    
    
    name, ext = os.path.splitext(uploaded_file.name)
    new_name = hashlib.md5(
        '%s%f' % (get_random_string(), time.time())
    ).hexdigest()
    new_name = '%s%s' % (new_name, ext.lower())
    
    fpath = os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, new_name)
    
    with open(fpath, 'w') as f:
        for c in uploaded_file.chunks(10240):
            f.write(c)
            
            
    # uploaed image has been saved on disk, now save it name in db
    if UploadedImage.objects.filter(uid=get_uid(request)).exists():
        UploadedImage.objects.filter(uid=get_uid(request)).update(image=new_name)
    else:
        UploadedImage.objects.create(uid=get_uid(request), image=new_name)
        
    print UPLOAD_AVATAR_URL_PREFIX_ORIGINAL + new_name
    return HttpResponse(
        "<script>window.parent.upload_avatar_success('%s')</script>" % \
        (UPLOAD_AVATAR_URL_PREFIX_ORIGINAL + new_name)
    )


@protected
def crop_avatar(request):
    try:
        upim = UploadedImage.objects.get(uid=get_uid(request))
    except UploadedImage.DoesNotExist:
        raise UploadAvatarError('upload again')
    
    image_orig = upim.get_image_path()
    if not image_orig:
        raise UploadAvatarError('upload again')
    
    x1 = int(request.POST['x1'])
    y1 = int(request.POST['y1'])
    x2 = int(request.POST['x2'])
    y2 = int(request.POST['y2'])
    
    
    orig = Image.open(image_orig)
    orig_w, orig_h = orig.size
    if orig_w <= 300 and orig_h <= 300:
        ratio = 1
    else:
        if orig_w > orig_h:
            ratio = float(orig_w) / 300
        else:
            ratio = float(orig_h) / 300
            
    box = [int(x * ratio) for x in [x1, y1, x2, y2]]
    avatar = orig.crop(box)
    avatar = avatar.resize((UPLOAD_AVATAR_RESIZE_SIZE, UPLOAD_AVATAR_RESIZE_SIZE), Image.ANTIALIAS)
    
    avatar_name, _ = os.path.splitext(upim.image)
    avatar_name = '%s-%d.%s' % (avatar_name, UPLOAD_AVATAR_RESIZE_SIZE, UPLOAD_AVATAR_SAVE_FORMAT)
    avatar_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, avatar_name)
    
    avatar.save(avatar_path, UPLOAD_AVATAR_SAVE_FORMAT, quality=UPLOAD_AVATAR_SAVE_QUALITY)
    print 'save done'
    
    avatar_crop_done.send(sender=None, uid=get_uid(request), avatar_name=avatar_name)
    if UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP:
        upim.delete()
        print 'delete...'
        
    return HttpResponse(
        "<script>window.parent.crop_avatar_success('done...')</script>" 
    )
