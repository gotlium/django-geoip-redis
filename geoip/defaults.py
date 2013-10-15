# -*- coding: utf-8 -*-

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


# Values: 'mysql' or 'redis'
BACKEND = get_settings("GEO_BACKEND", 'redis')

REDIS_HOST = getattr(settings, 'GEO_REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'GEO_REDIS_PORT', 6379)
REDIS_PASSWORD = getattr(settings, 'GEO_REDIS_PASSWORD', None)
REDIS_DB = getattr(settings, 'GEO_REDIS_DB', 0)

USE_CELERY = getattr(settings, 'GEO_USE_CELERY',
                     'djcelery' in settings.INSTALLED_APPS)
