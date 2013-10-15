# -*- coding: utf-8 -*-

from redis import StrictRedis
from geoip import defaults


class RedisClient(StrictRedis):
    def __init__(self):
        super(RedisClient, self).__init__(
            host=defaults.REDIS_HOST,
            port=defaults.REDIS_PORT,
            db=defaults.REDIS_DB,
            password=defaults.REDIS_PASSWORD)
