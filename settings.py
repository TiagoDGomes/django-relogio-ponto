# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
import os
from decouple import config
from decouple import Csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DATABASE_NAME', default=os.path.join(BASE_DIR, 'database.sqlite') ),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default='',),
        
    }
}

TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')
SECRET_KEY = config('SECRET_KEY', )
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')
STATIC_URL = config('STATIC_URL', default='/static/')

USE_I18N = True
USE_L10N = True
#USE_TZ = True
USE_TZ = False




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wsgi.application'


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



LOGIN_URL = '/admin/login/'

import sys
reload(sys)
exec "sys.setdefaultencoding('utf8')"

TOTAL_PAGINACAO = 10




TEST_RELOGIO_PONTO_TIPO = config('TEST_RELOGIO_PONTO_TIPO',default=0, cast=int)
TEST_RELOGIO_PONTO_ENDERECO = config('TEST_RELOGIO_PONTO_ENDERECO', default=None)
TEST_RELOGIO_PONTO_PORTA = config('TEST_RELOGIO_PONTO_PORTA', default=0, cast=int)




