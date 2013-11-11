Installation
============

Compatibility
-------------
* Python: 2.6, 2.7, 3.3
* Django: 1.3.x, 1.4.x, 1.5.x, 1.6


Recommended way to install is via pip::

  pip install django-geoip-redis


.. _basic:

Basic
-----

* Add ``geoip`` to ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (
        ...
        'geoip',
        ...
    )

* Create application tables on database::

    python manage.py syncdb

  If you're using South::

    python manage.py migrate


* Get latest data to perform geoip detection by :ref:`running management command <update>`::

    python manage.py update_geo_db


.. _advanced:

Advanced
--------

In order to make :ref:`user's location detection automatic <highlevel>` several other steps are required:

* Add ``GeoMiddleware`` to ``MIDDLEWARE_CLASSES``::

    MIDDLEWARE_CLASSES = (
        ...
        'geoip.middleware.GeoMiddleware',
    )

