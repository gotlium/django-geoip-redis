# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from geoip.models import Range


class IpGeoBase(object):
    SOURCE_URL = 'http://ipgeobase.ru/files/db/Main/geo_files.zip'

    FILE_FIELDS_DELIMITER = "\t"
    FILE_ENCODING = 'windows-1251'

    CITIES_FILENAME = 'cities.txt'
    CITIES_FIELDS = ['city_id', 'city_name', 'region_name', 'district_name', 'longitude', 'latitude']

    CIDR_FILENAME = 'cidr_optim.txt'
    CIDR_FIELDS = ['start_ip', 'end_ip', 'ip_range_human', 'country_code', 'city_id']

    def __init__(self):
        # todo: download here
        pass

    def get_cities(self):
        pass

    def get_range(self):
        pass


class UpdateGeoDB():
    def __init__(self):
        self.geo = IpGeoBase()


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        UpdateGeoDB().run()
