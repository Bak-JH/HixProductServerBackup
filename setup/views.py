import fnmatch
import json
import os
import zipfile

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def load_zipfile():
    target_dir = os.path.join(settings.BASE_DIR, "setup/")#TODO: edit path
    for filename in os.listdir(target_dir):
        if fnmatch.fnmatch(filename, "*DentSlicer*.zip"):
            with zipfile.ZipFile(os.path.abspath(target_dir + filename), 'r') as unzip:
                for name in unzip.namelist():
                    if fnmatch.fnmatch(name, "*.json"):
                        with unzip.open(name) as infoFile:
                            settings.LATEST_INFO = json.load(infoFile)
                    if fnmatch.fnmatch(name, "*.exe"):
                        with unzip.open(name) as exe:
                            settings.setupFile = os.path.abspath(unzip.extract(name, 'setup'))


def download_slicer(request):
    load_zipfile()
    with open(settings.setupFile, 'r+b') as fp:
        data = fp.read()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=DentSlicerSetup.exe"
    response.write(data)

    return response


def get_latest(request):
    load_zipfile()
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
