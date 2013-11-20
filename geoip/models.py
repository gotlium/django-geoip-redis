# -*- coding: utf-8 -*-

import sys

from django.db.models.signals import post_save, m2m_changed
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db import models

from geoip.redis_wrapper import RedisSync
from geoip.tasks import link_provider_task
from geoip.defaults import BACKEND


class Country(models.Model):
    code = models.CharField(_('Country code'), max_length=2, primary_key=True)
    name = models.CharField(_('Country name'), max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Area(models.Model):
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    name = models.CharField(_('Area'), max_length=255)
    # code = models.CharField(_('Area code'), max_length=3)
    # region_code = models.CharField(_('Region code'), max_length=2)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')
        unique_together = (('country', 'name'), )


class City(models.Model):
    area = models.ForeignKey(Area)
    name = models.CharField(_('City name'), max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        unique_together = (('area', 'name'), )


class ISP(models.Model):
    name = models.CharField('ISP', max_length=75)
    country = models.ForeignKey(Country, verbose_name=_('Country'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('ISP')
        verbose_name_plural = _("ISP's")
        unique_together = (('country', 'name'), )


class Provider(models.Model):
    name = models.CharField(_('Provider'), max_length=255, unique=True)
    isp = models.ManyToManyField(ISP, blank=True, verbose_name=_('ISP'))
    ranges = models.TextField(
        _('Provider network ranges'), blank=True, null=True)

    def add_isp(self, isp):
        if isp and not self.isp.filter(pk=isp.pk).exists():
            self.isp.add(isp)
            self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _("Providers")


class NetSpeed(models.Model):
    name = models.CharField(_('NetSpeed'), max_length=10, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Net Speed')
        verbose_name_plural = _("Net Speed")


class Domain(models.Model):
    name = models.CharField(_('Domain name'), max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Domain name')
        verbose_name_plural = _("Domain names")


class Range(models.Model):
    start_ip = models.BigIntegerField(_('Start range'), db_index=True)
    end_ip = models.BigIntegerField(_('End range'), db_index=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'))
    area = models.ForeignKey(Area, verbose_name=_('Area'), null=True)
    city = models.ForeignKey(City, verbose_name=_('City'), null=True)
    isp = models.ForeignKey(ISP, verbose_name=_('ISP'), null=True)
    provider = models.ForeignKey(
        Provider, verbose_name=_('Provider'), null=True)
    speed = models.ForeignKey(NetSpeed, verbose_name=_('NetSpeed'), null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        verbose_name=_('Latitude'))
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True,
        verbose_name=_('Longitude'))
    postal_code = models.CharField(
        _('Postal code'), max_length=6, blank=True, null=True)
    metro_code = models.PositiveIntegerField(
        _('Metro code'), blank=True, null=True)
    domain = models.ForeignKey(Domain, verbose_name=_('Domain'), null=True)

    @classmethod
    def by(cls, start, end):
        return cls.objects.filter(
            start_ip__lte=start, end_ip__gte=end
        ).order_by('end_ip', '-start_ip')

    @classmethod
    def sync_with_redis(cls):
        sync = RedisSync()
        sync.clean_all()
        for obj in cls.objects.all().order_by('id'):
            sync.sync_instance(obj)

    def set_provider(self, provider):
        self.provider = provider
        self.save()

    class Meta:
        verbose_name = _('IP range')
        verbose_name_plural = _("IP ranges")


if BACKEND == 'redis':
    @receiver(post_save, sender=Range, dispatch_uid="range")
    def save_to_redis(sender, instance, *args, **kwargs):
            RedisSync().sync_instance(instance)


if not 'loaddata' in sys.argv:
    @receiver(m2m_changed, sender=Provider.isp.through, dispatch_uid="prov")
    def save_provider(sender, instance, action, *args, **kwargs):
        if action == 'post_clear':
            link_provider_task(instance)
