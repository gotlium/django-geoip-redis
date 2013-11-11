Performance
===========

* django-geoip-redis:
    - MySQL(SSD): 728 rps
    - SQLite(SSD): 46 rps
    - Redis: **3548 rps**

* django-geoip(no isp, no provider):
    - MySQL(SSD): 855 rps
    - SQLite(SSD): 47 rps

* django.contrib.gis.geoip.GeoIP(no isp, no provider, but C API):
    - standard: 4666 rps
    - memory: 73 rps
    - check: 4510 rps
    - index: 76 rps
    - mmap: 4425 rps

Tested on Ubuntu 12.04(x86_64), Django(1.6), uWSGI(1.0.3), Nginx(1.1.19) with Apache Benchmark:

.. code-block:: bash

    $ ab -c 100 -n 1000 http://localhost/ip/91.195.136.52/


| On tests used default configuration for Redis & MySQL without any modifications.

