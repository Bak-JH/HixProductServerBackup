import fnmatch
import json
import os
import mimetypes

# Create your views here.
from django.conf import settings
from django.http import HttpResponse

def get_update_manifest(request, product_name):
    target_path = os.path.join(settings.UPDATE_FILE_DIR, product_name)
    data = sorted(os.listdir(target_path))
    return HttpResponse(json.dumps(data))

def get_file(request, product_name, file_name):
    target_path = os.path.join(settings.UPDATE_FILE_DIR, product_name)

    response = HttpResponse(content_type='application/force-download')

    try:
        with open(os.path.join(target_path + "/" + file_name)) as file:
            data = file.read()
    except:
        with open(os.path.join(target_path + "/" + file_name), 'r+b') as bin_file:
            data = bin_file.read()

    response.write(data)
    return response



