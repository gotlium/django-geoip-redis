Installation for development
============================

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

    >>> from geoip import record_by_ip_as_dict
    >>> print (record_by_ip_as_dict('91.195.136.52'))


If you want use native db for local development,
you can add ``GEO_BACKEND = 'db'`` into local_settings.py

