Django-GeoIP-Redis
==================

.. image:: https://api.travis-ci.org/gotlium/django-geoip-redis.png?branch=master
    :target: https://travis-ci.org/gotlium/django-geoip-redis
.. image:: https://coveralls.io/repos/gotlium/django-geoip-redis/badge.png?branch=master
    :target: https://coveralls.io/r/gotlium/django-geoip-redis?branch=master
.. image:: https://pypip.in/v/django-geoip-redis/badge.png
    :target: https://crate.io/packages/django-geoip-redis/
.. image:: https://pypip.in/d/django-geoip-redis/badge.png
    :target: https://crate.io/packages/django-geoip-redis/

Documentation available at `Read the Docs <http://django-geoip-redis.readthedocs.org/>`_.

Demo installation:
------------------

.. code-block:: bash

    $ sudo apt-get install redis-server virtualenvwrapper
    $ mkvirtualenv django-geoip-redis
    $ git clone https://github.com/gotlium/django-geoip-redis.git
    $ cd django-geoip-redis
    $ pip install -r requirements/package.txt
    $ python setup.py develop
    $ cd demo
    $ pip install -r requirements.txt
    $ python manage.py syncdb --noinput
    $ python manage.py migrate
    $ python manage.py loaddata ../fixtures/db.json
    $ python manage.py shell


.. code-block:: python

    >>> from geoip.geo import record_by_ip_as_dict
    >>> print (record_by_ip_as_dict('91.195.136.52'))


If you want use native db for local development,
you can add ``GEO_BACKEND = 'db'`` into local_settings.py


Performance:
-----------
* django-geoip-redis:
    - PostgreSQL(SSD): 85 rps
    - SQLite(SSD): 46 rps
    - MySQL(SSD): 728 rps
    - PostgreSQL: 63 rps
    - SQLite: 19 rps
    - MySQL: 349 rps
    - Redis: **3548 rps**

* django-geoip(no isp, no provider, no netspeed, no domain):
    - MySQL(SSD): 855 rps
    - SQLite(SSD): 47 rps

* django.contrib.gis.geoip.GeoIP(no isp, no provider, no netspeed, no domain, not free, but C API):
    - standard: 4666 rps
    - memory: 73 rps
    - check: 4510 rps
    - index: 76 rps
    - mmap: 4425 rps

Tested on Ubuntu 12.04(x86_64), Django(1.6), uWSGI(1.0.3), Nginx(1.1.19) with Apache Benchmark:

.. code-block:: bash

    $ ab -c 100 -n 1000 http://localhost/ip/91.195.136.52/


| On tests used default configuration for PostgreSQL, MySQL & Redis without any modifications.
|
| Demo page available `here <http://geoip-gotlium.rhcloud.com/ip/91.195.136.52/>`_.


Compatibility:
-------------
* Python: 2.6, 2.7, 3.3
* Django: 1.3.x, 1.4.x, 1.5.x, 1.6


.. image:: https://d2weczhvl823v0.cloudfront.net/gotlium/django-geoip-redis/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

