# -*- encoding: utf-8 -*-

import tempfile
import zipfile
import decimal

import os
import io

import requests

from geoip.models import Range, City, Area, Country
from geoip.backends.iso3166_1 import ISO_CODES
from geoip.redis_wrapper import RedisSync

SOURCE_URL = 'http://ipgeobase.ru/files/db/Main/geo_files.zip'
DB_FILE_NAME = '/tmp/geo_files.zip'
CIDR_FIELDS = [
    'start_ip', 'end_ip', 'ip_range_human', 'country_code', 'city_id']
CITIES_FIELDS = [
    'city_id', 'city_name', 'area_name',
    'district_name', 'latitude', 'longitude']


class IpGeoBase(object):
    def clean_database(self):
        Range.objects.all().delete()
        City.objects.all().delete()
        Area.objects.all().delete()
        Country.objects.all().delete()

    def clean_redis(self):
        sync = RedisSync()
        sync.clean_all()

    def clear_database(self):
        self.clean_database()
        self.clean_redis()

    def download_files(self):
        if os.path.exists(DB_FILE_NAME):
            os.unlink(DB_FILE_NAME)
        open(DB_FILE_NAME, 'w').write(requests.get(SOURCE_URL).content)
        if not os.path.exists(DB_FILE_NAME):
            raise Exception('File is not downloaded')

    def extract_archive(self):
        archive = zipfile.ZipFile(DB_FILE_NAME)
        temp_dir = tempfile.mkdtemp()
        file_cities = archive.extract('cities.txt', path=temp_dir)
        file_cidr = archive.extract('cidr_optim.txt', path=temp_dir)
        return {'cities': file_cities, 'cidr': file_cidr}

    def _extract_data_from_line(self, line, field_names=None, delimiter="\t"):
        return dict(zip(field_names, line.rstrip('\n').split(delimiter)))

    def _line_to_dict(self, file, field_names):
        for line in file:
            yield self._extract_data_from_line(line, field_names)

    def _get_country_code_for_city(self, city_id, mapping, added_data):
        try:
            return mapping[city_id]
        except KeyError:
            return added_data[-1]['country__code']

    def _process_cidr_file(self, file):
        data = {'cidr': [], 'countries': set(), 'city_country_mapping': {}}

        for cidr_info in self._line_to_dict(file, field_names=CIDR_FIELDS):
            city_id = None
            if cidr_info['city_id'] != '-':
                city_id = cidr_info['city_id']

            if city_id is not None:
                data['city_country_mapping'].update(
                    {cidr_info['city_id']: cidr_info['country_code']}
                )

            data['cidr'].append({
                'start_ip': cidr_info['start_ip'],
                'end_ip': cidr_info['end_ip'],
                'country_id': cidr_info['country_code'],
                'city_id': city_id
            })
            data['countries'].add(cidr_info['country_code'])
        return data

    def _process_cities_file(self, file, city_country_mapping):
        data = {
            'all_areas': [], 'areas': [],
            'cities': [], 'city_area_mapping': {}}

        for geo_info in self._line_to_dict(file, field_names=CITIES_FIELDS):
            country_code = self._get_country_code_for_city(
                geo_info['city_id'], city_country_mapping, data['all_areas'])

            new_area = {
                'name': geo_info['area_name'], 'country__code': country_code}

            if new_area not in data['all_areas']:
                data['all_areas'].append(new_area)

            if new_area not in data['areas']:
                data['areas'].append(new_area)

            data['cities'].append({
                'area__name': geo_info['area_name'],
                'name': geo_info['city_name'],
                'id': geo_info['city_id'],
                'latitude': decimal.Decimal(geo_info['latitude']),
                'longitude': decimal.Decimal(geo_info['longitude'])
            })
        return data

    def _build_city_area_mapping(self):
        cities = City.objects.values('id', 'area__id')
        city_area_mapping = {}
        for city in cities:
            if city['id']:
                city_area_mapping.update({city['id']: city['area__id']})
        return city_area_mapping

    def _update_cidr(self, cidr):
        new_ip_ranges = []
        is_bulk_create_supported = hasattr(Range.objects, 'bulk_create')
        Range.objects.all().delete()
        city_area_mapping = self._build_city_area_mapping()

        for entry in cidr['cidr']:
            if entry['city_id']:
                entry.update({
                    'area_id': city_area_mapping[int(entry['city_id'])]})
            if is_bulk_create_supported:
                new_ip_ranges.append(Range(**entry))
            else:
                Range.objects.create(**entry)
        if is_bulk_create_supported:
            Range.objects.bulk_create(new_ip_ranges)

    def _update_geography(
            self, countries, areas, cities, city_country_mapping):
        existing = {
            'cities': list(City.objects.values_list('id', flat=True)),
            'areas': list(Area.objects.values('name', 'country__code')),
            'countries': Country.objects.values_list('code', flat=True)
        }
        for country_code in countries:
            if country_code not in existing['countries']:
                Country.objects.create(
                    code=country_code,
                    name=ISO_CODES.get(country_code, country_code)
                )

        for entry in areas:
            if entry not in existing['areas']:
                Area.objects.create(
                    name=entry['name'], country_id=entry['country__code'])

        for entry in cities:
            if int(entry['id']) not in existing['cities']:
                code = city_country_mapping.get(entry['id'])
                if code:
                    area = Area.objects.get(
                        name=entry['area__name'], country__code=code)
                    City.objects.create(
                        id=entry['id'], name=entry['name'], area=area,
                        latitude=entry.get('latitude'),
                        longitude=entry.get('longitude'))

    def sync_database(self):
        files = self.extract_archive()
        cidr_info = self._process_cidr_file(
            io.open(files['cidr'], encoding='windows-1251'))
        city_info = self._process_cities_file(
            io.open(files['cities'], encoding='windows-1251'),
            cidr_info['city_country_mapping'])
        self._update_geography(cidr_info['countries'],
                               city_info['areas'],
                               city_info['cities'],
                               cidr_info['city_country_mapping'])
        self._update_cidr(cidr_info)
