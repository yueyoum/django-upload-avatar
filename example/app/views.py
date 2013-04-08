# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

upload_folder = os.path.join(settings.PROJECT_PATH, 'upload')
if not os.path.isdir(upload_folder):
    os.mkdir(upload_folder)



def get_upload_images(request, filename):
    if filename.endswith(('.jpg', '.jpep')):
        mimetype = 'image/jpeg'
    elif filename.endswith('.png'):
        mimetype = 'image/png'
    elif filename.endswith('.gif'):
        mimetype = 'image/gif'
        
        
    with open(os.path.join(upload_folder, filename), 'r') as f:
        return HttpResponse(f.read(), mimetype=mimetype)



@csrf_exempt
def upload(request):
    return render_to_response(
        'upload.html',
        context_instance = RequestContext(request)
    )
