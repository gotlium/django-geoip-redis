# -*- coding: utf-8 -*-

import json

from django.utils.functional import SimpleLazyObject
from django.conf import settings


def get_location(request):
    """
    Cache on Cookies is not a best practice and insecure, but very faster.
    You can redeclare this behavior on your project or rewrite that.
    """
    if not hasattr(request, 'cached_geo'):
        stored = request.get_signed_cookie('cached_geo', None)
        if stored is not None:
            return json.loads(stored)

    from geoip.geo import record_by_request_as_dict
    return record_by_request_as_dict(request)


class GeoMiddleware(object):
    def process_request(self, request):
        request.geo = SimpleLazyObject(lambda: get_location(request))

    def process_response(self, request, response):
        if not hasattr(request, 'geo'):
            return response
        response.set_signed_cookie('cached_geo', json.dumps(dict(request.geo)))
        return response


class LocalIPFix(object):
    """
    IP & SSL emulation
    """
    def process_request(self, request):
        if getattr(settings, 'DEBUG', False):
            request.META['REMOTE_ADDR'] = getattr(
                settings, 'LOCAL_IP_FIX', '91.195.136.52')

            if getattr(settings, 'LOCAL_SSL', False):
                request.META['HTTP_X_FORWARDED_SSL'] = 'on'
                request.is_secure = lambda: True
