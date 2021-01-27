from __future__ import absolute_import, unicode_literals



"""
Django settings for slicerServer project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
UPDATE_FILE_DIR = os.path.join(BASE_DIR, 'SetupFiles')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lpuy*em0gp)2pr5mvxaptp@(7x1iuq0_+gwa+_l^8#q!o&-kq+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # default sample code ends here
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.naver',
    'corsheaders',
    'channels',
    'crispy_forms',
    'rest_framework',
    'django_email_verification',

    'slicerServer',
    'product',
    'setup',
    'management',
    'resin',
    'posts',
    'taggit',
    'taggit_autosuggest',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'slicerServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'slicerServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '../static/'

# Redirect to home URL after login (Default redirects to /accounts/profile/)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
#mine, for testing
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'palesminion1@gmail.com'
# EMAIL_HOST_PASSWORD = 'PALESpalla123'



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    )



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    # 'naver': {
	# 	'AUTH_PARAMS': {'response_type': 'code'},
	# }
}


ASGI_APPLICATION = "slicerServer.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ),
# }

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://hix.co.kr',
    'https://services.hix.co.kr',
]

CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS  = ['hix.co.kr', 'services.hix.co.kr']
CSRF_COOKIE_DOMAIN = '.hix.co.kr'

EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = 'support@hix.co.kr'
EMAIL_PASSWORD = '*hix20130829'

EMAIL_FROM_ADDRESS = 'HiX<support@hix.co.kr>'
EMAIL_MAIL_SUBJECT = 'Confirm your email'
EMAIL_MAIL_HTML = 'auth_mail.html'
# EMAIL_MAIL_PLAIN = 'auth_mail.txt'
# EMAIL_TOKEN_LIFE = 60 * 3
EMAIL_PAGE_TEMPLATE = 'confirm_mail.html'
EMAIL_PAGE_DOMAIN = 'http://services.hix.co.kr/'

# # For Django Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'support@hix.co.kr'
# EMAIL_HOST_PASSWORD = '*hix20130829'
# EMAIL_USE_TLS = True

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 120960000
SESSION_COOKIE_DOMAIN = '.hix.co.kr'
SESSION_COOKIE_HTTPONLY = True
SESSION_DOMAIN_NAME = 'hix.co.kr'
SESSION_COOKIE_SECURE = True

ACCOUNT_SESSION_REMEMBER = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

RECAPTCHA_SITE_KEY = "6LcBdgcaAAAAACT2L3b6-5uugc0W2Xlr3i62Hpq3"
RECAPTCHA_SECRET_KEY = "6LcBdgcaAAAAAAjMT3qeFySEmu1e4yyqJCmE6Lxo"


# ACCOUNT_EMAIL_REQUIRED = True


