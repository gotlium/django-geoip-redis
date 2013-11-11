# -*- coding: utf-8 -*-

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


# Values: 'db' or 'redis'
BACKEND = get_settings("GEO_BACKEND", 'redis')

REDIS_HOST = getattr(settings, 'GEO_REDIS_HOST', 'localhost')
REDIS_PORT = getattr(settings, 'GEO_REDIS_PORT', 6379)
REDIS_PASSWORD = getattr(settings, 'GEO_REDIS_PASSWORD', None)
# db: 1 = name, db: 2 = pk
REDIS_DB = getattr(settings, 'GEO_REDIS_DB', 1)

USE_CELERY = getattr(settings, 'GEO_USE_CELERY',
                     'djcelery' in settings.INSTALLED_APPS)

# Values: 'name' or 'pk'
REDIS_TYPE = getattr(settings, 'GEO_REDIS_TYPE',
                     'pk' if REDIS_DB == 2 else 'name')
REDIS_SYNC_LOCK = getattr(settings, 'REDIS_SYNC_LOCK', '/tmp/redis.lock')

DB_IMPORT_URL = getattr(
    settings, 'GEO_DB_IMPORT_URL',
    'http://geo-gotlium.rhcloud.com/db.json.zip')
