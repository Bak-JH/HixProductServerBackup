from django.conf import settings
import os
import json

filename = os.path.join(settings.BASE_DIR, "setup/update_info.json")
with open(filename, "r") as json_file:
    settings.LATEST_INFO = json.load(json_file)
    settings.LATEST_INFO['exe'] = os.path.join(settings.BASE_DIR, "setup/templates/DentSlicerSetup.exe")
