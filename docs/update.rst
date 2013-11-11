.. _update:

Updating GeoIP database
=======================

.. note::
    Currentrly ``django-geoip-redis`` supports only ipgeobase.ru backend.

To update your database:::

    python manage.py update_geo_db


.. warning::
    This is irreversible operation, do not use on production!

.. note::
    If you're having ``2006, 'MySQL server has gone away'`` error during database update,
    setting ``max_allowed_packet`` to a higher value might help.
    E.g. ``max_allowed_packet=16M``
