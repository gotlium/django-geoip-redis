# -*- coding: utf-8 -*-

from django.utils.functional import SimpleLazyObject


def get_location(request):
    """
    Cache on Cookies is not a best practice and insecure, but very faster.
    You can redeclare this behavior on your project or rewrite that.
    """
    if not hasattr(request, 'cached_geo'):
        stored = request.get_signed_cookie('cached_geo', None)
        if stored is not None:
            return stored

        from geoip import record_by_request

        request.cached_geo = record_by_request(request)
        request.COOKIES['cached_geo'] = request.cached_geo
    return request.cached_geo


class GeoMiddleware(object):
    def process_request(self, request):
        request.geo = SimpleLazyObject(lambda: get_location(request))

    def process_response(self, request, response):
        if not hasattr(request, 'geo'):
            return response
        response.set_signed_cookie('cached_geo', request.geo)
        return response
