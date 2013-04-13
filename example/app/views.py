# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from upload_avatar.app_settings import (
    UPLOAD_AVATAR_UPLOAD_ROOT,
    UPLOAD_AVATAR_AVATAR_ROOT,
    UPLOAD_AVATAR_RESIZE_SIZE,
)

from upload_avatar import get_uploadavatar_context

from .models import User


#########################
# In production, you don't need this,
# static files should serve by web server, e.g. Nginx

def find_mimetype(filename):
    """In production, you don't need this,
    Static files should serve by web server, e.g. Nginx.
    """
    if filename.endswith(('.jpg', '.jpep')):
        return 'image/jpeg'
    if filename.endswith('.png'):
        return 'image/png'
    if filename.endswith('.gif'):
        return 'image/gif'
    return 'application/octet-stream'


def get_upload_images(request, filename):
    mimetype = find_mimetype(filename)
    with open(os.path.join(UPLOAD_AVATAR_UPLOAD_ROOT, filename), 'r') as f:
        return HttpResponse(f.read(), mimetype=mimetype)
    
def get_avatar(request, filename):
    mimetype = find_mimetype(filename)
    with open(os.path.join(UPLOAD_AVATAR_AVATAR_ROOT, filename), 'r') as f:
        return HttpResponse(f.read(), mimetype=mimetype)


#########################



@login_required
def home(request):
    try:
        u = User.objects.get(user_id=request.user.id)
    except User.DoesNotExist:
        html = '<html><body><a href="/upload">upload avatar</a></body></html>'
        return HttpResponse(html)
    
    imgs = map(lambda size: "<p><img src='%s'/></p>" % u.get_avatar_url(size), UPLOAD_AVATAR_RESIZE_SIZE)
    
    html = """<html>
    <body>
    <h2>%s <a href="/upload">upload avatar</a></h2>
    %s
    </boby>
    </html>""" % (request.user.username, '\n'.join(imgs))
    return HttpResponse(html)



@login_required
def upload(request):
    return render_to_response(
        'upload.html',
        get_uploadavatar_context(),
        context_instance = RequestContext(request)
    )

