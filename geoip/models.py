# -*- coding: utf-8 -*-

from django.db import models


class Country(models.Model):
    code = models.CharField('Country code', max_length=2, primary_key=True)
    name = models.CharField('Country name', max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Area(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField('Area', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Area'
        unique_together = (('country', 'name'), )


class City(models.Model):
    area = models.ForeignKey(Area)
    name = models.CharField('City name', max_length=255)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        unique_together = (('area', 'name'), )


class ISP(models.Model):
    name = models.CharField('ISP', max_length=255)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'ISP'
        verbose_name_plural = "ISP's"
        unique_together = (('country', 'name'), )


class Provider(models.Model):
    name = models.CharField('Provider', max_length=255, unique=True)
    isp = models.ManyToManyField(ISP)
    ranges = models.TextField(u'Provider ip ranges')

    def add_isp(self, isp):
        self.isp.add(isp)
        self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class Range(models.Model):
    start_ip = models.BigIntegerField('Start', db_index=True)
    end_ip = models.BigIntegerField('End', db_index=True)
    country = models.ForeignKey(Country)
    area = models.ForeignKey(Area, null=True)
    city = models.ForeignKey(City, null=True)
    isp = models.ForeignKey(ISP, null=True)
    provider = models.ForeignKey(Provider, null=True)

    @classmethod
    def by(cls, start, end):
        return cls.objects.filter(start_ip__lte=start, end_ip__gte=end)

    def set_provider(self, provider):
        self.provider = provider
        self.save()

    class Meta:
        verbose_name = 'IP range'
        verbose_name_plural = "IP ranges"
