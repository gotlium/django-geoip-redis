# -*- coding: utf-8 -*-

import zipfile

from django.core.management.base import NoArgsCommand

from geoip.models import Range, City, Area, Country
import StringIO
import requests
import tempfile


ISO_CODES = {
    "AF": "Afghanistan",
    "AX": "Åland",
    "AL": "Albania",
    "DZ": "Algeria",
    "AS": "American Samoa",
    "AD": "Andorra",
    "AO": "Angola",
    "AI": "Anguilla",
    "AQ": "Antarctica",
    "AG": "Antigua and Barbuda",
    "AR": "Argentina",
    "AM": "Armenia",
    "AW": "Aruba",
    "AU": "Australia",
    "AT": "Austria",
    "AZ": "Azerbaijan",
    "BS": "Bahamas",
    "BH": "Bahrain",
    "BD": "Bangladesh",
    "BB": "Barbados",
    "BY": "Belarus",
    "BE": "Belgium",
    "BZ": "Belize",
    "BJ": "Benin",
    "BM": "Bermuda",
    "BT": "Bhutan",
    "BO": "Bolivia",
    "BQ": "Bonaire, Sint Eustatiusand Saba",
    "BA": "Bosnia and Herzegovina",
    "BW": "Botswana",
    "BV": "Bouvet Island",
    "BR": "Brazil",
    "IO": "British Indian Ocean Territory",
    "BN": "Brunei Darussalam",
    "BG": "Bulgaria",
    "BF": "Burkina Faso",
    "BI": "Burundi",
    "KH": "Cambodia",
    "CM": "Cameroon",
    "CA": "Canada",
    "CV": "Cape Verde",
    "KY": "Cayman Islands",
    "CF": "Central African Republic",
    "TD": "Chad",
    "CL": "Chile",
    "CN": "China",
    "CX": "Christmas Island",
    "CC": "Cocos (Keeling) Islands",
    "CO": "Colombia",
    "KM": "Comoros",
    "CG": "Congo (Brazzaville)",
    "CD": "Congo (Kinshasa)",
    "CK": "Cook Islands",
    "CR": "Costa Rica",
    "CI": "Côte d'Ivoire",
    "HR": "Croatia",
    "CU": "Cuba",
    "CW": "Curaçao",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DJ": "Djibouti",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "EC": "Ecuador",
    "EG": "Egypt",
    "SV": "El Salvador",
    "GQ": "Equatorial Guinea",
    "ER": "Eritrea",
    "EE": "Estonia",
    "ET": "Ethiopia",
    "FK": "Falkland Islands",
    "FO": "Faroe Islands",
    "FJ": "Fiji",
    "FI": "Finland",
    "FR": "France",
    "GF": "French Guiana",
    "PF": "French Polynesia",
    "TF": "French Southern Lands",
    "GA": "Gabon",
    "GM": "Gambia",
    "GE": "Georgia",
    "DE": "Germany",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GR": "Greece",
    "GL": "Greenland",
    "GD": "Grenada",
    "GP": "Guadeloupe",
    "GU": "Guam",
    "GT": "Guatemala",
    "GG": "Guernsey",
    "GN": "Guinea",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HT": "Haiti",
    "HM": "Heard and McDonald Islands",
    "HN": "Honduras",
    "HK": "Hong Kong",
    "HU": "Hungary",
    "IS": "Iceland",
    "IN": "India",
    "ID": "Indonesia",
    "IR": "Iran",
    "IQ": "Iraq",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IL": "Israel",
    "IT": "Italy",
    "JM": "Jamaica",
    "JP": "Japan",
    "JE": "Jersey",
    "JO": "Jordan",
    "KZ": "Kazakhstan",
    "KE": "Kenya",
    "KI": "Kiribati",
    "KP": "Korea, North",
    "KR": "Korea, South",
    "KW": "Kuwait",
    "KG": "Kyrgyzstan",
    "LA": "Laos",
    "LV": "Latvia",
    "LB": "Lebanon",
    "LS": "Lesotho",
    "LR": "Liberia",
    "LY": "Libya",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MO": "Macau",
    "MK": "Macedonia",
    "MG": "Madagascar",
    "MW": "Malawi",
    "MY": "Malaysia",
    "MV": "Maldives",
    "ML": "Mali",
    "MT": "Malta",
    "MH": "Marshall Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MU": "Mauritius",
    "YT": "Mayotte",
    "MX": "Mexico",
    "FM": "Micronesia",
    "MD": "Moldova",
    "MC": "Monaco",
    "MN": "Mongolia",
    "ME": "Montenegro",
    "MS": "Montserrat",
    "MA": "Morocco",
    "MZ": "Mozambique",
    "MM": "Myanmar",
    "NA": "Namibia",
    "NR": "Nauru",
    "NP": "Nepal",
    "NL": "Netherlands",
    "NC": "New Caledonia",
    "NZ": "New Zealand",
    "NI": "Nicaragua",
    "NE": "Niger",
    "NG": "Nigeria",
    "NU": "Niue",
    "NF": "Norfolk Island",
    "MP": "Northern Mariana Islands",
    "NO": "Norway",
    "OM": "Oman",
    "PK": "Pakistan",
    "PW": "Palau",
    "PS": "Palestine",
    "PA": "Panama",
    "PG": "Papua New Guinea",
    "PY": "Paraguay",
    "PE": "Peru",
    "PH": "Philippines",
    "PN": "Pitcairn",
    "PL": "Poland",
    "PT": "Portugal",
    "PR": "Puerto Rico",
    "QA": "Qatar",
    "RE": "Reunion",
    "RO": "Romania",
    "RU": "Russian Federation",
    "RW": "Rwanda",
    "BL": "Saint Barthélemy",
    "SH": "Saint Helena",
    "KN": "Saint Kitts and Nevis",
    "LC": "Saint Lucia",
    "MF": "Saint Martin (French part)",
    "PM": "Saint Pierre and Miquelon",
    "VC": "Saint Vincent and theGrenadines",
    "WS": "Samoa",
    "SM": "San Marino",
    "ST": "Sao Tome and Principe",
    "SA": "Saudi Arabia",
    "SN": "Senegal",
    "RS": "Serbia",
    "SC": "Seychelles",
    "SL": "Sierra Leone",
    "SG": "Singapore",
    "SX": "Sint Maarten",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "SB": "Solomon Islands",
    "SO": "Somalia",
    "ZA": "South Africa",
    "GS": "South Georgia and South Sandwich Islands",
    "SS": "South Sudan",
    "ES": "Spain",
    "LK": "Sri Lanka",
    "SD": "Sudan",
    "SR": "Suriname",
    "SJ": "Svalbard and Jan Mayen Islands",
    "SZ": "Swaziland",
    "SE": "Sweden",
    "CH": "Switzerland",
    "SY": "Syria",
    "TW": "Taiwan",
    "TJ": "Tajikistan",
    "TZ": "Tanzania",
    "TH": "Thailand",
    "TL": "Timor-Leste",
    "TG": "Togo",
    "TK": "Tokelau",
    "TO": "Tonga",
    "TT": "Trinidad and Tobago",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TM": "Turkmenistan",
    "TC": "Turks and Caicos Islands",
    "TV": "Tuvalu",
    "UG": "Uganda",
    "UA": "Ukraine",
    "AE": "United Arab Emirates",
    "GB": "United Kingdom",
    "UM": "United States Minor Outlying Islands",
    "US": "United States of America",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VU": "Vanuatu",
    "VA": "Vatican City",
    "VE": "Venezuela",
    "VN": "Vietnam",
    "VG": "Virgin Islands, British",
    "VI": "Virgin Islands, U.S.",
    "WF": "Wallis and Futuna Islands",
    "EH": "Western Sahara",
    "YE": "Yemen",
    "ZM": "Zambia",
    "ZW": "Zimbabwe",
}


class IpGeoBase(object):
    SOURCE_URL = 'http://ipgeobase.ru/files/db/Main/geo_files.zip'

    FILE_FIELDS_DELIMITER = "\t"
    FILE_ENCODING = 'windows-1251'

    CITIES_FILENAME = 'cities.txt'
    CITIES_FIELDS = ['city_id', 'city_name', 'region_name', 'district_name',
                     'longitude', 'latitude']

    CIDR_FILENAME = 'cidr_optim.txt'
    CIDR_FIELDS = ['start_ip', 'end_ip', 'ip_range_human', 'country_code',
                   'city_id']

    def __init__(self):
        self.files = self.download_and_extract()

    def download_and_extract(self):
        archive = zipfile.ZipFile(self.download())
        temp_dir = tempfile.mkdtemp()
        file_cities = archive.extract(self.CITIES_FILENAME, path=temp_dir)
        file_cidr = archive.extract(self.CIDR_FILENAME, path=temp_dir)
        return {'cities': file_cities, 'cidr': file_cidr}

    def download(self):
        r = requests.get(self.SOURCE_URL)
        return StringIO.StringIO(r.content)

    def get_data(self, filekey, fields):
        for line in open(self.files[filekey]).readlines():
            if not line:
                continue
            line = line.decode(self.FILE_ENCODING, 'utf8')
            yield dict(zip(
                fields, line.strip().split(self.FILE_FIELDS_DELIMITER)))

    def get_cities(self):
        return self.get_data('cities', self.CITIES_FIELDS)

    def get_ranges(self):
        return self.get_data('cidr', self.CIDR_FIELDS)

    def __del__(self):
        import os

        os.unlink(self.files['cidr'])
        os.unlink(self.files['cities'])


class UpdateGeoDB():
    def __init__(self):
        self.geo = IpGeoBase()
        self._countries = {}
        self._cities = {}

    def clean(self):
        Range.objects.all().delete()
        City.objects.all().delete()
        Area.objects.all().delete()
        Country.objects.all().delete()

    def _get_db(self, store, key, klass, **kwargs):
        value = store.get(key)
        if value is not None:
            return value
        store[key] = klass.objects.get(kwargs)
        return store.get(key)

    def get_country(self, key):
        return self._get_db(self._countries, key, Country, code=key)

    def get_city(self, key):
        if key != '-':
            return self._get_db(self._cities, key, City, pk=key)
            #return City.objects.get(pk=key)

    def save_area_and_city(self):
        for row in self.cities:
            print row['city_name']
            '''
            #region = Area.objects.get(name=row['region__name'])
            area = Area.objects.get_or_create(name=row['region_name'])[0]

            City.objects.create(
                latitude=row.get('latitude'), longitude=row.get('longitude'),
                id=row.get('city_id'), name=row.get('city_name'),
                area=area,
                #region=region,
            )

            #print row.get('district_name')
            pass
            '''

    def save_country(self):
        for row in self.geo.get_ranges():
            Range.objects.create(
                start_ip=row.get('start_ip'),
                end_ip=row.get('end_ip'),
                country=self.get_country(row.get('country_code')),
                city=self.get_city(row.get('city_id')),
            )

    def save_countries(self):
        for code, name in ISO_CODES.items():
            self._countries[code] = Country.objects.create(
                code=code, name=name)

    def map_ranges_with_cities(self):
        self.cities = {}
        self.ranges = []

        for row in self.geo.get_cities():
            self.cities[row.get('city_id')] = row

        for row in self.geo.get_ranges():
            city_id = row.get('city_id')
            if city_id:
                print row['country_code']
                self.cities[city_id]['country_code'] = row['country_code']
            self.ranges.append(row)

    def run(self):
        #self.clean()
        self.save_countries()
        self.map_ranges_with_cities()
        self.save_area_and_city()
        # self.get_country(row.get('country_code'))


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        UpdateGeoDB().run()
