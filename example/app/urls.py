# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    #url(r'^$', views.home, name="home"),
    url(r'^upload/?$', views.upload, name="upload"),
    url(r'^avatar/(?P<filename>.+)/?$', views.get_upload_images, name="avatar_url"),
)