import fnmatch
import json
import os

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def load_updateFile(target_dir):
    for (path, dir, files) in os.walk(target_dir):
        for filename in files:
            if fnmatch.fnmatch(filename, "*.json"):
                with open(os.path.join(path, filename)) as infoFile:
                    settings.LATEST_INFO = json.load(infoFile)
            if fnmatch.fnmatch(filename, "*.exe"):
                with open(os.path.join(path, filename)) as exe:
                    settings.setupFile = os.path.abspath(exe.name)


def download_slicer(request):
    load_updateFile(os.path.join(settings.BASE_DIR, "setup/"))#TODO: edit path
    with open(settings.setupFile, 'r+b') as fp:
        data = fp.read()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=DentSlicerSetup.exe"
    response.write(data)

    return response


def get_latest(request):
    load_updateFile(os.path.join(settings.BASE_DIR, "setup/"))#TODO: edit path
    file = render(request, os.path.join(settings.BASE_DIR, "setup/templates/appcast_template.html"),
                  {'release': settings.LATEST_INFO})
    return HttpResponse(file, content_type="application/xml")


def download_firmware(request):
    with open(os.path.join(settings.BASE_DIR, 'setup/DentSlicer-1.1.2.zip'), 'r+b') as fp: #TODO: edit path
        data = fp.read()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=FirmwareSetup.zip"
    response.write(data)

    return response
