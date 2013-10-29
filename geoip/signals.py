# -*- coding: utf-8 -*-

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from geoip.redis_wrapper import RedisSync
from geoip.tasks import link_provider_task
from geoip.defaults import BACKEND
from geoip.models import Provider
from geoip.models import Range


@receiver(post_save, sender=Range, dispatch_uid="range")
def save_to_redis(sender, instance, *args, **kwargs):
    if BACKEND == 'redis':
        RedisSync().sync_instance(instance)


@receiver(m2m_changed, sender=Provider.isp.through, dispatch_uid="provider")
def save_provider(sender, instance, action, *args, **kwargs):
    if action == 'post_clear':
        link_provider_task(instance)
