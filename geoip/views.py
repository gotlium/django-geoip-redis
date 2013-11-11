# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from geoip.provider import LinkIspWithProvider
from geoip.geo import record_by_ip
from geoip.defaults import BACKEND


def home(request):
    """
    If middleware was installed, you can get geo info from request.geo
    Example:
        print request.geo
    """
    return HttpResponse("""
        <a href="/ip/91.195.136.52/">IP info</a>
    """)


def ip_view(request, ip=None):
    ip = ip if ip else request.META.get('REMOTE_ADDR')
    record = record_by_ip(ip)
    if record:
        if BACKEND == 'db':
            data = (
                record.country, record.area,
                record.city, record.isp,
                record.provider
            )
        else:
            data = (
                record[0], record[1],
                record[2], record[3],
                record[4]
            )

        return HttpResponse(
            '%s, %s, %s, %s, %s' % data
        )
    return HttpResponse('No info about: %s' % ip)


def show_range_isp(request):
    link = LinkIspWithProvider()
    messages = []
    if request.method == 'POST':
        for line in request.POST.get('range').strip().split('\n'):
            link.ip = line.strip()
            line_isp = []

            for row in link.get_range():
                if row.isp is not None:
                    line_isp.append(
                        row.isp.name + u'(%s->%s)' % (
                            row.country, row.city))
                else:
                    line_isp.append(
                        u'unknown(%s->%s)' % (row.country, row.city))
            messages.append(
                line.decode('utf8') + u' - ' + u','.join(set(line_isp)))

    return render(request, 'geoip/range.html', {'messages': messages})
