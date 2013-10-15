# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver

from geoip.redis_wrapper import RedisClient
from geoip.tasks import link_provider_task
from geoip.defaults import BACKEND
from geoip.models import Provider
from geoip.models import Range


@receiver(post_save, sender=Range)
def save_to_redis(sender, instance, *args, **kwargs):
    if BACKEND == 'redis':
        redis = RedisClient()

        key = "%s:%d" % (instance.country.code, instance.pk)

        redis.zadd("geoip", "%s:s" % key, instance.start_ip)
        redis.zadd("geoip", "%s:e" % key, instance.end_ip)

        redis.hmset("geoip:%s" % instance.country, {
            "provider": instance.provider,
            "country": instance.country,
            "area": instance.area,
            "city": instance.city,
            "isp": instance.isp,
        })


@receiver(post_save, sender=Provider)
def save_provider(sender, instance, *args, **kwargs):
    link_provider_task(instance)
