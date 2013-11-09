# -*- coding: utf-8 -*-

from redis import Redis
from geoip import defaults


class RedisClient(Redis):
    def __init__(self):
        super(RedisClient, self).__init__(
            host=defaults.REDIS_HOST,
            port=defaults.REDIS_PORT,
            db=defaults.REDIS_DB,
            password=defaults.REDIS_PASSWORD)


class RedisSync(RedisClient):
    def __init__(self):
        super(RedisSync, self).__init__()
        self.instance = None
        self.key = ""

    def save_base(self):
        self.key = "%s:%d" % (self.instance.country.code, self.instance.pk)

        self.zadd("geoip", "%s:s" % self.key, self.instance.start_ip)
        self.zadd("geoip", "%s:e" % self.key, self.instance.end_ip)

    def _get_val(self, key):
        if not hasattr(getattr(self.instance, key), defaults.REDIS_TYPE):
            return '*'
        return getattr(getattr(self.instance, key), defaults.REDIS_TYPE)

    def save_data(self):
        self.set(
            "geoip:%d" % self.instance.pk,
            "%s:%s:%s:%s:%s" % (
                self._get_val('country'),
                self._get_val('area'),
                self._get_val('city'),
                self._get_val('isp'),
                self._get_val('provider'),
            )
        )

    def clean_all(self):
        self.flushdb()

    def sync_instance(self, instance):
        self.instance = instance
        self.save_base()
        self.save_data()
