# -*- coding: utf-8 -*-

from django.conf import settings

UPLOAD_AVATAR_UPLOAD_ROOT = settings.UPLOAD_AVATAR_UPLOAD_ROOT
UPLOAD_AVATAR_URL_PREFIX = settings.UPLOAD_AVATAR_URL_PREFIX


UPLOAD_AVATAR_MAX_SIZE = getattr(settings, 'UPLOAD_AVATAR_MAX_SIZE', 1024 * 1024 *3)

UPLOAD_AVATAR_TEST_FUNC = getattr(settings, 'UPLOAD_AVATAR_TEST_FUNC', None)
if UPLOAD_AVATAR_TEST_FUNC is None:
    def UPLOAD_AVATAR_TEST_FUNC(request):
        return request.method == 'POST' and 'Filedata' in request.FILES
    
UPLOAD_AVATAR_RESIZE_SIZE = getattr(settings, 'UPLOAD_AVATAR_CROP_SIZE', 50)