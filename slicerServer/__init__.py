from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os
import json

#이 구문은 shared_task를 위해 장고가 시작될 때 app이 항상 임포트 되도록 하는 역할을 합니다.
from setup.tasks import app as celery_app

__all__ = ('celery_app', )

filename = os.path.join(settings.BASE_DIR, "setup/update_info.json")
with open(filename, "r") as json_file:
    settings.LATEST_INFO = json.load(json_file)
    settings.LATEST_INFO['exe'] = os.path.join(settings.BASE_DIR, "setup/templates/DentSlicerSetup.exe")
