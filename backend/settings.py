"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'srt(vue=+gl&0c_c3pban6a&m2h2iz6mhbx^%^_%9!#-jg0*lz'

# SECURITY WARNING: don't run with debug turned on in production!
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
  'api',
  'rest_framework.authtoken',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'ON_HEROKU' in os.environ:
  # heroku database
  if 'ON_DEV' in os.environ:
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

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
#
# AUTH_PASSWORD_VALIDATORS = [
#   {
#     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#   },
#   {
#     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#   },
#   {
#     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#   },
#   {
#     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#   },
# ]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
AUTH_USER_MODEL = 'api.UserProfile'
