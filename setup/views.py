import fnmatch
import json
import os
import mimetypes

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve

def get_update_manifest(request, product_name):
    target_path = os.path.join(settings.UPDATE_FILE_DIR, product_name)
    data = sorted(os.listdir(target_path))
    return HttpResponse(json.dumps(data))

def get_file(request, product_name, file_name):
    target_path = os.path.join(settings.UPDATE_FILE_DIR, product_name)
    return serve(request, os.path.basename(os.path.join(target_path, file_name)), os.path.dirname(os.path.join(target_path, file_name)))

def view_file(request, product_name, file_name):
    target_path = os.path.join(settings.UPDATE_FILE_DIR, product_name)

    if 'xml' in file_name:
        response = HttpResponse(content_type='application/xml')
    else:
        response = HttpResponse(content_type='text/html')

    with open(os.path.join(target_path + "\\" + file_name)) as file:
        data = file.read()

    response.write(data)
    return response
