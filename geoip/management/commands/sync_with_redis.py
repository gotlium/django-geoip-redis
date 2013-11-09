# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from geoip.models import Range


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        Range.sync_with_redis()
