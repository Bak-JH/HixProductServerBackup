from django.conf import settings
import os
import json

filename = os.path.join(settings.BASE_DIR, "setup/update_info.json")
with open(filename, "r") as json_file:
    settings.latest_info = json.load(json_file)
    settings.latest_info['exe'] = os.path.join(settings.BASE_DIR, "setup/templates/DentSlicerSetup.exe")
