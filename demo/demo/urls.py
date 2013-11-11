from django.conf.urls import patterns, include, url
from django.shortcuts import HttpResponse
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'', include('geoip.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
