# -*- coding: utf-8 -*-

from celery.task import Task

from geoip.management.commands.update_geo_db import UpdateGeoDB
from geoip.provider import LinkIspWithProvider
from geoip.defaults import USE_CELERY


class LinkIspWithProviderTask(Task):
    def run(self, *args, **kwargs):
        LinkIspWithProvider().run(*args, **kwargs)


class UpdateDatabaseTask(Task):
    def run(self, *args, **kwargs):
        UpdateGeoDB().run()


def _do_task(cls, *args, **kwargs):
    (cls.delay if USE_CELERY else cls.run)(*args, **kwargs)


def update_database(*args, **kwargs):
    _do_task(UpdateDatabaseTask, *args, **kwargs)


def link_provider_task(*args, **kwargs):
    _do_task(LinkIspWithProviderTask, *args, **kwargs)
