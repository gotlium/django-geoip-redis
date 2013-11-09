# -*- coding: utf-8 -*-

from django.test import TestCase

from geoip.models import Range
from geoip import geo


class GeoIPTestCase(TestCase):
    fixtures = ['tests_fixture.json']

    def test_redis(self):
        geo.BACKEND = 'redis'
        ip_range = geo.record_by_addr('91.195.136.52')
        self.assertTrue(isinstance(ip_range, list))
        self.assertListEqual(
            ['RU', '102', '1878', '4835', '1'],
            geo.record_by_addr('91.195.136.52')
        )

    def test_db(self):
        geo.BACKEND = 'db'
        ip_range = geo.record_by_addr('91.195.136.52')
        self.assertTrue(isinstance(ip_range, Range))
        self.assertEqual(ip_range.pk, 61045)
