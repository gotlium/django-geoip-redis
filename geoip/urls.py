# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns(
    'geoip.views',
    url(r'^ip/$', 'ip_view', name='geoip-view'),
    url(r'^ip/(?P<ip>.*?)/$', 'ip_view', name='geoip-by-ip-view'),
)
