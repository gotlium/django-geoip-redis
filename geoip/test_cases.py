# -*- coding: utf-8 -*-

from django.test import TestCase

from geoip import geo, defaults


LIST_DATA = [
    'RU', '102', '1878', '4835', '1', '', '36.069492', '52.968452',
    '', '', ''
]

EXISTING_IP = '91.195.136.52'
NOT_EXISTING_IP = '194.85.91.253'


# todo: add tests for home, ip_view & show_range_isp views
# todo: tests for LinkIspWithProvider
# todo: tests for Middleware
# todo: geo.py tests
# todo: tests for celery queue
# todo: sync tests
class GeoIPTestCase(TestCase):
    fixtures = ['tests_fixture.json']

    def _test_rule(self, backend, ip, data):
        geo.BACKEND = backend
        self.assertListEqual(data, geo.record_by_ip(ip))

    def test_redis(self):
        self._test_rule('redis', EXISTING_IP, LIST_DATA)

    def test_redis_default(self):
        self._test_rule('redis', NOT_EXISTING_IP, defaults.DEFAULT_LOCATION)

    def test_db(self):
        self._test_rule('db', EXISTING_IP, LIST_DATA)

    def test_db_default(self):
        self._test_rule('db', NOT_EXISTING_IP, defaults.DEFAULT_LOCATION)
