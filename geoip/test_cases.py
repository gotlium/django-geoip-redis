# -*- coding: utf-8 -*-

from django.test import TestCase

from geoip import geo, defaults


LIST_DATA = [
    'RU', '102', '1878', '4835', '1', '*', '36.069492', '52.968452',
    '*', '*', '*'
]


class GeoIPTestCase(TestCase):
    fixtures = ['tests_fixture.json']

    def test_a_redis(self):
        geo.BACKEND = 'redis'
        ip_range = geo.record_by_ip('91.195.136.52')
        self.assertListEqual(LIST_DATA, ip_range)

    def test_b_redis_default(self):
        geo.BACKEND = 'redis'
        ip_range = geo.record_by_ip('194.85.91.253')
        self.assertListEqual(defaults.DEFAULT_LOCATION, ip_range)

    def test_c_db(self):
        geo.BACKEND = 'db'
        ip_range = list(geo.record_by_ip('91.195.136.52'))
        self.assertListEqual(LIST_DATA, ip_range)

    def test_d_db_default(self):
        geo.BACKEND = 'db'
        ip_range = list(geo.record_by_ip('194.85.91.253'))
        self.assertListEqual(defaults.DEFAULT_LOCATION, ip_range)
