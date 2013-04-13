# -*- coding: utf-8 -*-

version_info = (0, 1, 0)
VERSION = __version__ = '.'.join( map(str, version_info) )

def get_uploadavatar_context():
    from .app_settings import UPLOAD_AVATAR_WEB_LAYOUT, UPLOAD_AVATAR_TEXT
    
    uploadavatar_context = UPLOAD_AVATAR_WEB_LAYOUT.copy()
    uploadavatar_context.update(UPLOAD_AVATAR_TEXT)
    return uploadavatar_context



