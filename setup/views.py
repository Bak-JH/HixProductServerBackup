from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
import os, json

def read_file():
    filename = os.path.join(settings.BASE_DIR, "setup/update_info.json")
    with open(filename, "r") as json_file:
        settings.LATEST_INFO = json.load(json_file)

def download_file(request):
    # fill these variables with real values
    read_file()
    with open(settings.LATEST_INFO['exe'], 'r+b') as fp:
        data = fp.read()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=DentSlicerSetup.exe"
    response.write(data)

    return response

def get_latest(request):
    read_file()
    file = render(request, os.path.join(settings.BASE_DIR, "setup/templates/appcast_template.html"),
                  {'release': settings.LATEST_INFO})
    return HttpResponse(file, content_type="application/xml")
