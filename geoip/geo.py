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

    res, score = r.zrangebyscore("geoip", ip, 'inf', 0, 1, withscores=True)[0]
    geo_id, junk, prefix = res.split(":", 2)

    if prefix == "s" and float(score) > ip:
        return

    return r.hgetall("geoip:" + geo_id)


def _from_db(ip):
    return Range.objects.filter(
        start_ip__lte=ip, end_ip__gte=ip
    ).order_by('end_ip', '-start_ip')[:1][0]


def record_by_addr(ip):
    (_from_redis if BACKEND == 'redis' else _from_db)(inet_aton(ip))
