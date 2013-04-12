# -*- coding: utf-8 -*-
import os

from django.conf import settings

# where the uploaded image store, absolute path
UPLOAD_AVATAR_UPLOAD_ROOT = settings.UPLOAD_AVATAR_UPLOAD_ROOT

# where the cropped avatar store, absolute path
UPLOAD_AVATAR_AVATAR_ROOT = settings.UPLOAD_AVATAR_AVATAR_ROOT


if not os.path.isdir(UPLOAD_AVATAR_UPLOAD_ROOT):
    os.mkdir(UPLOAD_AVATAR_UPLOAD_ROOT)
if not os.path.isdir(UPLOAD_AVATAR_AVATAR_ROOT):
    os.mkdir(UPLOAD_AVATAR_AVATAR_ROOT)


# URL prefix for the original uploaded image
# e.g. uploadedimage/ or image/ ...
UPLOAD_AVATAR_URL_PREFIX_ORIGINAL = settings.UPLOAD_AVATAR_URL_PREFIX_ORIGINAL

# URL prefix for the cropped, real avatar
# e.g. avatar/
UPLOAD_AVATAR_URL_PREFIX_CROPPED = settings.UPLOAD_AVATAR_URL_PREFIX_CROPPED

# Yes, you noticed there are two URLs,
# URL_PREFIX_ORIGINAL just used after user upload an image,
# and the web will shown the uploaded image for select the crop area.
#
# URL_PREFIX_CROPPED is actually  used for user avatar 


# Default max allowed size is 3MB
UPLOAD_AVATAR_MAX_SIZE = getattr(settings, 'UPLOAD_AVATAR_MAX_SIZE', 1024 * 1024 *3)

# You should custom the test function.
# test function take 'request' as the only argument.
# It controls whether this request is valid and call the view function
# Default test function as you see, just ensure that the 'POST' method and verify the user
# you can do more tests.
UPLOAD_AVATAR_TEST_FUNC = getattr(settings, 'UPLOAD_AVATAR_TEST_FUNC', None)
if UPLOAD_AVATAR_TEST_FUNC is None:
    UPLOAD_AVATAR_TEST_FUNC = lambda request: request.method == 'POST' and \
                              request.user.is_authenticated()

# If you are using custom user, and the user object isn't `request.user`
# you should define this function, for me to know how get the uid from request
# this function take `request` as argument, and return the current logged user's id
UPLOAD_AVATAR_GET_UID_FUNC = getattr(settings, 'UPLOAD_AVATAR_GET_UID_FUNC', None)
if UPLOAD_AVATAR_GET_UID_FUNC is None:
    UPLOAD_AVATAR_GET_UID_FUNC = lambda request: request.user.id
    
    
    

# How many different size your wanna resize.
# NOTICE, the value MUST be list, even if there are only one size.
UPLOAD_AVATAR_RESIZE_SIZE = getattr(settings, 'UPLOAD_AVATAR_CROP_SIZE', [50,])

# Avatar default size which will be shown in you website,
# this is for call user.get_avatar_path(), user.get_avatar_url() more convenient
UPLOAD_AVATAR_DEFAULT_SIZE = getattr(settings, 'UPLOAD_AVATAR_DEFAULT_SIZE', 50)

# Avatar format, you can also choose: jpep, gif...
UPLOAD_AVATAR_SAVE_FORMAT = getattr(settings, 'UPLOAD_AVATAR_SAVE_FORMAT', 'png')
if UPLOAD_AVATAR_SAVE_FORMAT == 'jpg':
    UPLOAD_AVATAR_SAVE_FORMAT = 'jpeg'

UPLOAD_AVATAR_SAVE_QUALITY = getattr(settings, 'UPLOAD_AVATAR_SAVE_QUALITY', 90)


# Whethe delete the uploaded original image after avatar cropped, default is True
UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP = getattr(settings, 'UPLOAD_AVATAR_DELETE_ORIGINAL_AFTER_CROP', True)



# Bellow settings are for web layout and text shown in web or javascript alert
# Why not using i18n?
# first, i18n will reduce django performance
# second, If this app using i18n, But your project not, what you will do? Enable i18n JUST for this app?


UPLOAD_AVATAR_WEB_LAYOUT = {
    'crop_image_area_size': 300,
    
    'preview_areas': [
        {
            'size': 50,
            'text': 'Small Preview'
        },
        {
            'size': 120,
            'text': 'Large Preview'
        },
    ]
}

UPLOAD_AVATAR_TEXT = {
    'CHOOSE_IMAGE': 'Choose Image',
    'CROP_IMAGE': 'Crop',
    'TEST_FUNC_NOT_PASSED': 'Forbidden',
    'INVALID_IMAGE': 'Invalid File, Please choose an image',
    'NO_IMAGE': 'Please upload image',
    'TOO_LARGE': 'File Too Large, choose a smaller one',
    'SUCCESS': 'Success',
    'ERROR': 'Error, try later',
}

UPLOAD_AVATAR_WEB_LAYOUT.update(
    getattr(settings, 'UPLOAD_AVATAR_WEB_LAYOUT', {})
)

UPLOAD_AVATAR_TEXT.update(
    getattr(settings, 'UPLOAD_AVATAR_TEXT', {})
)