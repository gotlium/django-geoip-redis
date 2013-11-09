# -*- coding: utf-8 -*-

import struct
import socket

from geoip.redis_wrapper import RedisClient
from geoip.defaults import BACKEND
from geoip.models import Range


def inet_aton(ip):
    return struct.unpack('!L', socket.inet_aton(ip))[0]


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
        return info.decode().split(':')


def _from_db(ip):
    return Range.objects.filter(
        start_ip__lte=ip, end_ip__gte=ip
    ).order_by('end_ip', '-start_ip')[:1][0]


def record_by_addr(ip):
    return (_from_redis if BACKEND == 'redis' else _from_db)(inet_aton(ip))
