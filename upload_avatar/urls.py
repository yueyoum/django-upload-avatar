# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


from . import views

urlpatterns = patterns('',
    url(r'^uploadavatar_upload/?$', views.upload_avatar),
    url(r'^uploadavatar_crop/?$', views.crop_avatar),
)