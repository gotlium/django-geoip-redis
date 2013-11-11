.. _settings:

Settings
========

``django-geoip-redis`` has some configuration:

.. code-block:: python

    # Values: 'db' or 'redis'
    GEO_BACKEND = 'redis'
    GEO_USE_CELERY = False

    GEO_REDIS_HOST = 'localhost'
    GEO_REDIS_PORT = 6379
    GEO_REDIS_PASSWORD = None
    GEO_REDIS_DB = 1

    # Values: 'name' or 'pk'
    GEO_REDIS_TYPE = 'name'

