# -*- encoding: utf-8 -*-

from optparse import make_option

from django.core.management.base import BaseCommand
from geoip.backends.ipgeobase import IpGeoBase


class Command(BaseCommand):
    help = 'Update django-geoip-redis data stored in db'

    option_list = BaseCommand.option_list + (
        make_option(
            '--clear',
            action='store_true',
            default=False,
            help="Clear tables prior import"
        ),
    )

    def handle(self, *args, **options):
        backend = IpGeoBase()

        if options.get('clear'):
            backend.clear_database()

        backend.download_files()
        backend.sync_database()
