# -*- coding: utf-8 -*-

__all__ = ["inet_aton", "record_by_ip", "record_by_request", "get_ip",
           "record_by_ip_as_dict", "record_by_request_as_dict"]

import struct
import socket

from geoip.defaults import BACKEND, REDIS_TYPE
from geoip.redis_wrapper import RedisClient
from geoip.models import Range


_RECORDS_KEYS = ('country', 'area', 'city', 'isp', 'provider')


def _from_redis(ip):
    r = RedisClient()

    data = r.zrangebyscore("geoip", ip, 'inf', 0, 1, withscores=True)

    if not data:
        return

    res, score = data[0]
    geo_id, junk, prefix = res.decode().split(":", 2)

    if prefix == "s" and score > ip:
        return

    info = r.get("geoip:%s" % junk)
    if info is not None:
        return info.decode('utf-8', 'ignore').split(':')


def _from_db(ip):
    obj = Range.objects.select_related().filter(
        start_ip__lte=ip, end_ip__gte=ip
    ).order_by('end_ip', '-start_ip')[:1][0]
    if REDIS_TYPE == 'pk':
        return map(lambda k: str(getattr(obj, k).pk), _RECORDS_KEYS)
    return map(lambda k: str(getattr(obj, k)), _RECORDS_KEYS)


def inet_aton(ip):
    return struct.unpack('!L', socket.inet_aton(ip))[0]


def get_ip(request):
    ip = request.META['REMOTE_ADDR']
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    return ip


def record_by_ip(ip):
    return (_from_redis if BACKEND == 'redis' else _from_db)(inet_aton(ip))


def record_by_request(request):
    return record_by_ip(get_ip(request))


def record_by_ip_as_dict(ip):
    return dict(zip(_RECORDS_KEYS, record_by_ip(ip)))


def record_by_request_as_dict(request):
    return dict(zip(_RECORDS_KEYS, record_by_ip(get_ip(request))))
