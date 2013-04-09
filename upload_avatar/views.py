# -*- coding: utf-8 -*-

import os
import hashlib
import time
from functools import wraps

from PIL import Image

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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


def protected(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not test_func(request):
            print 'test failure'
            print request.user
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return deco


@csrf_exempt
@protected
def upload_avatar(request):
    try:
        uploaded_file = request.FILES['Filedata']
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
    UploadedImage.objects.create(uid=get_uid(request), image=new_name)
    
    return HttpResponse(UPLOAD_AVATAR_URL_PREFIX_ORIGINAL + new_name, mimetype='text/plain')


@csrf_exempt
@protected
def crop_avatar(request):
    try:
        upim = UploadedImage.objects.get(uid=get_uid(request))
    except UploadedImage.DoesNotExist:
        return HttpResponse(status=403)
    
    image_orig = upim.get_image_path()
    if not image_orig:
        return HttpResponse(status=403)
    
    x1 = int(request.POST['x1'])
    y1 = int(request.POST['y1'])
    x2 = int(request.POST['x2'])
    y2 = int(request.POST['y2'])
    
    orig = Image.open(image_orig)
    avatar = orig.crop([x1, y1, x2, y2])
    
    avatar.resize((UPLOAD_AVATAR_RESIZE_SIZE, UPLOAD_AVATAR_RESIZE_SIZE), Image.ANTIALIAS)
    
    avatar_name, _ = os.path.splitext(upim.image)
    avatar_name = '%s-%d.%s' % (avatar_name, UPLOAD_AVATAR_RESIZE_SIZE, UPLOAD_AVATAR_SAVE_FORMAT)
    avatar_path = os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, avatar_name)
    
    avatar.save(avatar_path, UPLOAD_AVATAR_SAVE_FORMAT, quality=UPLOAD_AVATAR_SAVE_QUALITY)
    print 'save done'
    
    avatar_crop_done.send(sender=None, uid=get_uid(request), avatar_name=avatar_name)
    if UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP:
        upim.delete()
        
    return HttpResponse()
