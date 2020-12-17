import urllib
import json
from django.conf import settings

def verify_recaptcha(recaptcha_response):
    # captcha verification
    data = {
        'response': recaptcha_response,
        'secret': settings.RECAPTCHA_SECRET_KEY
    }
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data)

    # verify the token submitted with the form is valid
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    # result will be a dict containing 'success' and 'action'.
    # it is important to verify both
    
    if (not result['success']) or (not result['action'] == 'signup'):
        return False

    return True
    # end captcha verification