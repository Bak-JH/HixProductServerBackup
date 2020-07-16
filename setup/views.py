from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse
import os

def download_file(request):
    # fill these variables with real values
    with open(settings.LATEST_INFO['exe'], 'r+b') as fp:
        data = fp.read()
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = "attachment; filename=DentSlicerSetup.exe"
    response.write(data)

    return response

def get_latest(request):
    file = render(request, os.path.join(settings.BASE_DIR, "setup/templates/appcast_template.html"),
                  {'release': settings.LATEST_INFO})
    return HttpResponse(file, content_type="application/xml")
