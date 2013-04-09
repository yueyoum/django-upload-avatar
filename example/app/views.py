# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


from upload_avatar.app_settings import UPLOAD_AVATAR_UPLOAD_ROOT, UPLOAD_AVATAR_AVATAR_ROOT, UPLOAD_AVATAR_URL_PREFIX_CROPPED

from .models import User


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



@login_required
def home(request):
    try:
        u = User.objects.get(user_id=request.user.id)
    except User.DoesNotExist:
        html = '<html><body><a href="/upload">upload avatar</a></body></html>'
        return HttpResponse(html)
    
    html = """<html>
    <body>
    <h2>%s</h2>
    <img src="%s" />
    </boby>
    </html>""" % (request.user.username, UPLOAD_AVATAR_URL_PREFIX_CROPPED + u.avatar_name)
    return HttpResponse(html)



@login_required
def upload(request):
    return render_to_response(
        'upload.html',
        context_instance = RequestContext(request)
    )
