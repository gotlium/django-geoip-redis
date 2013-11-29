# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from geoip.provider import LinkIspWithProvider
from geoip.geo import record_by_ip, get_ip


def home(request):
    """
    If middleware was installed, you can get geo info from request.geo
    Example:
        print request.geo
    """
    # todo: move into template form, and print request.geo, if info was found
    middleware_info = ', '.join(request.geo.values()) if request.geo else ''
    return HttpResponse("""
        <a href="/ip/91.195.136.52/">Information by given IP</a>
        <p><strong>Default location or auto-detected:</strong> %s</p>
    """ % middleware_info)


def ip_view(request, ip=None):
    record = record_by_ip(ip if ip else get_ip(request))
    if record is not None:
        return HttpResponse(','.join(record))
    return HttpResponse('No data found')


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
