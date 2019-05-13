"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

#  rlcapp - record and organization management software for refugee law clinics
#  Copyright (C) 2019  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

import os
import django_heroku
from datetime import timedelta, timezone
import boto
from boto.s3.connection import OrdinaryCallingFormat, Location


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'srt(vue=+gl&0c_c3pban6a&m2h2iz6mhbx^%^_%9!#-jg0*lz'

# SECURITY WARNING: don't run with debug turned on in production!
if 'ON_HEROKU' in os.environ and 'DEBUG' in os.environ:
    DEBUG = os.environ['DEBUG']
else:
    DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'backend.api',
    'backend.recordmanagement',
    'rest_framework.authtoken',
    'storages',
    #'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'


# Default settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'backend.api.authentication.ExpiringTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'backend.api.exception_handler.custom_exception_handler',
}
# Authentication Timeout
if 'ON_HEROKU' in os.environ:
    TIMEOUT_TIMEDELTA = timedelta(minutes=10)
else:
    TIMEOUT_TIMEDELTA = timedelta(weeks=10)


# Templates
if 'ON_HEROKU' in os.environ:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['static'],
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
else:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['static/dev', 'static'],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
if 'ON_HEROKU' in os.environ:
    # heroku database
    if 'ON_DEPLOY' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ['DB_NAME'],  # database
                'USER': os.environ['DB_USER'],  # user
                'PASSWORD': os.environ['DB_PASSWORD'],  # password
                'HOST': os.environ['DB_HOST'],  # part of uri, after @ before :, or host
                'PORT': os.environ['DB_PORT'],  # port
            }
        }
    elif 'ON_DEV' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'dd804idbj534r1',
                'USER': 'hnegrdmxsdnsdg',
                'PASSWORD': '85f8d3c19c4d8791b8d3ddc61848e84d0e7fdaa1015a8c1f9d06b12f192f166c',
                'HOST': 'ec2-54-247-79-32.eu-west-1.compute.amazonaws.com',
                'PORT': '5432',
            }
        }
    elif 'ON_TEST' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'db29qk1cvplv1b',
                'USER': 'oxnphgrugnpugu',
                'PASSWORD': '4f25e6ee4581095852494124d7aab7ca6bed3be9f0eeb0152bc58f292abbc7c9',
                'HOST': 'ec2-54-217-218-80.eu-west-1.compute.amazonaws.com',
                'PORT': '5432',
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# heroku and authentication
django_heroku.settings(locals())
AUTH_USER_MODEL = 'api.UserProfile'

# email
if 'ON_HEROKU' in os.environ or 'EMAIL_HOST' in os.environ:
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_PORT = os.environ['EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_USER_TLS = os.environ['EMAIL_USER_TLS']
    EMAIL_USE_SSL = os.environ['EMAIL_USE_SSL']
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# storage
if 'ON_HEROKU' in os.environ and os.environ['ON_HEROKU']:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    COMPRESS_STORAGE = 'backend.shared.storage_generator.CachedS3Boto3Storage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_S3_BUCKET_NAME
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = 'private'
AWS_S3_SIGV4 = True
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'
# AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
# GZIP
if 'ON_HEROKU' in os.environ and os.environ['ON_HEROKU']:
    AWS_IS_GZIPPED = True
    GZIP_CONTENT_TYPES = (
        'text/css',
        'application/javascript',
        'application/x-javascript',
        'text/javascript',
        'text/jscript',
        'text/ecmascript',
        'application/ecmascript'
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_LOCATION = 'static'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if 'ON_HEROKU' in os.environ and os.environ['ON_HEROKU']:
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    COMPRESS_URL = STATIC_URL
else:
    STATIC_URL = '/static/'
