Django-GeoIP-Redis
==================

Demo installation:
$ mkvirtualenv django-geoip-redis
$ git clone https://github.com/gotlium/django-geoip-redis.git
$ cd django-geoip-redis
$ python setup.py develop
$ cd demo
$ pip install -r requirements.txt
$ python manage.py syncdb
$ python manage.py migrate
$ python manage.py loaddata ../fixtures/db.json
$ python manage.py runserver
$ python manage.py sync_with_redis
$ python manage.py shell

>>> from geoip import record_by_addr
>>> print ','.join(record_by_addr('91.195.136.52'))

If you want use native db for local development,
you can add ``GEO_BACKEND = 'db'`` into your local_settings.py



.. image:: https://d2weczhvl823v0.cloudfront.net/gotlium/django-geoip-redis/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

