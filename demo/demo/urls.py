from django.conf.urls import patterns, include, url
from django.shortcuts import HttpResponse
from django.contrib import admin

admin.autodiscover()


def home(request):
    return HttpResponse("""
    <a href="/ip/91.195.136.52/">IP info</a>
    """)


urlpatterns = patterns(
    '',
    url(r'', include('geoip.urls')),
    url(r'^$', home, name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
