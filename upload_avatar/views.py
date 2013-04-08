# -*- coding: utf-8 -*-

import os
import hashlib
import time
from functools import wraps

from PIL import Image

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from .app_settings import UPLOAD_AVATAR_TEST_FUNC as test_func
from .app_settings import UPLOAD_AVATAR_MAX_SIZE, UPLOAD_AVATAR_UPLOAD_ROOT, UPLOAD_AVATAR_URL_PREFIX, UPLOAD_AVATAR_RESIZE_SIZE

from .signals import avatar_crop_done


def protected(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not test_func(request):
            return HttpResponse(status=403)
        return func(request, *args, **kwargs)
    return deco


@csrf_exempt
@protected
def upload_avatar(request):
    uploaded_file = request.FILES['Filedata']
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
            
    request.session['avatar_orig'] = fpath
    return HttpResponse(UPLOAD_AVATAR_URL_PREFIX + new_name, mimetype='plain/text')


@csrf_exempt
@protected
def crop_avatar(request):
    avatar_orig = request.session.get('avatar_orig', None)
    if not avatar_orig or not os.path.exists(avatar_orig):
        return HttpResponse(status=403)
    
    x1 = int(request.POST['x1'])
    y1 = int(request.POST['y1'])
    x2 = int(request.POST['x2'])
    y2 = int(request.POST['y2'])
    
    orig = Image.open(avatar_orig)
    avatar_new = orig.crop([x1, y1, x2, y2])
    
    avatar_new.resize((UPLOAD_AVATAR_RESIZE_SIZE, UPLOAD_AVATAR_RESIZE_SIZE), Image.ANTIALIAS)
    avatar_new.save('/tmp/abc.png', 'png', quality=100)
    print 'save done'
    
    #avatar_crop_done.send()
