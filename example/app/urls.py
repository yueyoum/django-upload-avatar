# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from upload_avatar.app_settings import UPLOAD_AVATAR_URL_PREFIX_CROPPED, UPLOAD_AVATAR_URL_PREFIX_ORIGINAL

from . import views

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    url(r'^$', views.home, name="home"),
    url(r'^upload/?$', views.upload, name="upload"),
    url(r'%s(?P<filename>.+)/?$' % UPLOAD_AVATAR_URL_PREFIX_ORIGINAL,
        views.get_upload_images
        ),
    url(r'^%s(?P<filename>.+)/?$' % UPLOAD_AVATAR_URL_PREFIX_CROPPED,
        views.get_avatar
        )
)