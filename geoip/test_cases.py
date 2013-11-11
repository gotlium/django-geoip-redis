# -*- coding: utf-8 -*-

from django.test import TestCase

from geoip import geo


LIST_DATA = ['RU', '102', '1878', '4835', '1']


class GeoIPTestCase(TestCase):
    fixtures = ['tests_fixture.json']

    def test_redis(self):
        geo.BACKEND = 'redis'
        ip_range = geo.record_by_ip('91.195.136.52')
        self.assertListEqual(LIST_DATA, ip_range)

    def test_db(self):
        geo.BACKEND = 'db'
        ip_range = list(geo.record_by_ip('91.195.136.52'))
        self.assertListEqual(LIST_DATA, ip_range)
