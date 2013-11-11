# -*- coding: utf-8 -*-

try:
    from django.conf.urls.defaults import *
except ImportError:
    from django.conf.urls import *

urlpatterns = patterns(
    'geoip.views',
    url(r'^$', 'home', name='home-view'),
    url(r'^ip/$', 'ip_view', name='geoip-view'),
    url(r'^ip/(?P<ip>.*?)/$', 'ip_view', name='geoip-by-ip-view'),
    url(r'^range/$', 'show_range_isp', name='geoip-range-view'),
)
