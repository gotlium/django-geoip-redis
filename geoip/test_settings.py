# -*- coding: utf-8 -*-

from django import VERSION


DATABASE_ENGINE = 'sqlite3'

SITE_ID = 1

SECRET_KEY = 'cb452188a1c017e94f96d9f813ec2bf8'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'geoip',
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

if VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

GEO_REDIS_TYPE = 'pk'
GEO_REDIS_DB = 6
