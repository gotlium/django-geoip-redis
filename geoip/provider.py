# -*- coding: utf-8 -*-

import ipaddress

from geoip.geo import inet_aton
from geoip.models import Range


class LinkIspWithProvider():
    def __init__(self):
        self.ip = None
        self.provider = None

    def get_network(self):
        return ipaddress.ip_network(self.ip, strict=False)

    def get_start(self):
        return inet_aton(self.get_network().network_address)

    def get_end(self):
        return inet_aton(self.get_network().broadcast_address)

    def save(self):
        start = self.get_start()
        end = self.get_end()

        for ip_range in Range.by(start, end):
            ip_range.set_provider(self.provider)
            self.provider.add_isp(ip_range.isp)

    def run(self, instance):
        self.provider = instance
        for ip in instance.ranges.split("\n"):
            self.ip = unicode(ip)
