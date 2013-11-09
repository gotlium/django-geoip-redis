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
        return inet_aton(str(self.get_network().network_address))

    def get_end(self):
        return inet_aton(str(self.get_network().broadcast_address))

    def get_range(self):
        start = self.get_start()
        end = self.get_end()
        return Range.by(start, end)

    def save_ip(self):
        for ip_range in self.get_range():
            ip_range.set_provider(self.provider)
            self.provider.add_isp(ip_range.isp)

    def save_by_range(self):
        for ip in self.provider.ranges.strip().split("\n"):
            if ip:
                self.ip = ip
                self.save_ip()

    def save_by_isp(self):
        for isp in self.provider.isp.all():
            Range.objects.filter(isp=isp).update(provider=self.provider)

    def run(self, instance):
        self.provider = instance
        self.save_by_range()
        self.save_by_isp()
