import os

from django.conf.urls import patterns, url
from django.shortcuts import render
from django.contrib import admin

from geoip.models import *
from geoip.defaults import REDIS_SYNC_LOCK
from geoip.tasks import sync_redis_task


class ProviderAdmin(admin.ModelAdmin):
    filter_horizontal = ('isp',)

    def changelist_view(self, request, extra_context=None):
        self.change_list_template = 'geoip/admin/change_list_link.html'
        if not extra_context:
            extra_context = {}
        extra_context['lock'] = os.path.exists(REDIS_SYNC_LOCK)
        return super(ProviderAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def start_queue_view(self, request):
        sync_redis_task()
        return render(
            request, 'geoip/admin/sync.html', {
                'app_label': self.model._meta.app_label,
                'title': 'Sync with Redis',
                'message': 'Sync was started. Wait ...'
            }
        )

    def get_urls(self):
        urls = super(ProviderAdmin, self).get_urls()

        admin_urls = patterns(
            '',
            url(
                r'^sync_redis/$',
                self.admin_site.admin_view(self.start_queue_view),
                name='admin_do_start_redis_sync'
            ),
        )
        return admin_urls + urls


admin.site.register(Provider, ProviderAdmin)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(ISP)
admin.site.register(Range)
