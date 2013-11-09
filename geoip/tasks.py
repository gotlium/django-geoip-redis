# -*- coding: utf-8 -*-

import os

from celery.task import Task

from geoip.defaults import USE_CELERY, REDIS_SYNC_LOCK
from geoip.provider import LinkIspWithProvider
from geoip.models import Range


class LinkIspWithProviderTask(Task):
    def run(self, *args, **kwargs):
        LinkIspWithProvider().run(*args, **kwargs)


class SyncRedisTask(Task):
    def run(self, *args, **kwargs):
        try:
            if not os.path.exists(REDIS_SYNC_LOCK):
                open(REDIS_SYNC_LOCK, 'w').close()
                Range.sync_with_redis()
        except:
            pass

        os.unlink(REDIS_SYNC_LOCK)


def _do_task(cls, *args, **kwargs):
    (cls.delay if USE_CELERY else cls.run)(*args, **kwargs)


def sync_redis_task(*args, **kwargs):
    _do_task(SyncRedisTask(), *args, **kwargs)


def link_provider_task(*args, **kwargs):
    _do_task(LinkIspWithProviderTask(), *args, **kwargs)
