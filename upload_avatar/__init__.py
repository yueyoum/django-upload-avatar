# -*- coding: utf-8 -*-

from .app_settings import UPLOAD_AVATAR_WEB_LAYOUT, UPLOAD_AVATAR_TEXT

uploadavatar_context = UPLOAD_AVATAR_WEB_LAYOUT.copy()
uploadavatar_context['INVALID_IMAGE'] = UPLOAD_AVATAR_TEXT['INVALID_IMAGE']