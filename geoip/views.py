# -*- coding: utf-8 -*-

from django.http import HttpResponse
from geoip.geo import record_by_addr


def ip_view(request, ip=None):
    ip = ip if ip else request.META.get('REMOTE_ADDR')
    record = record_by_addr(ip)
    return HttpResponse(
        '%s, %s, %s, %s, %s' % (
            record.get('country'), record.get('area'),
            record.get('city'), record.get('isp'),
            record.get('provider')
        )
    )
