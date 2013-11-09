Django-GeoIP-Redis
==================

.. image:: https://api.travis-ci.org/gotlium/django-geoip-redis.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/gotlium/django-geoip-redis


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
    $ python manage.py sync_with_redis
    $ python manage.py shell


.. code-block:: python

    >>> from geoip import record_by_addr
    >>> print (','.join(record_by_addr('91.195.136.52')))


If you want use native db for local development,
you can add ``GEO_BACKEND = 'db'`` into local_settings.py


Performance:
-----------
* MySQL(SSD): 728 rps
* SQLite(SSD): 46 rps
* Redis: 3548 rps


Tested on Ubuntu 12.04(x86_64), Django(1.6), uWSGI(1.0.3), Nginx(1.1.19) with Apache Benchmark:


.. code-block:: bash

$ ab -c 100 -n 1000 http://localhost/ip/91.195.136.52/


Compatibility:
-------------
* Python: 2.6, 2.7, 3.3
* Django: 1.3.x, 1.4.x, 1.5.x, 1.6


.. image:: https://d2weczhvl823v0.cloudfront.net/gotlium/django-geoip-redis/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

