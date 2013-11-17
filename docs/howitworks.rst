Under the hood
==============

Data storage
------------

All geoip data, including geography and geoip mapping is stored in the database.
To avoid unnecessary database hits user location is stored in a cookie.

Geography
~~~~~~~~~

Django-geoip-redis supports only ipgeobase geography, which consist of following
entities: Country, Region, City. Database maintains normalized relationships
between all entities, i.e. Country has many Regions, Region has many Cities,
ISP has many Country, Provider has many ISP.

.. automodule:: geoip.models
   :members: Country, Area, City, ISP, Provider, NetSpeed


.. _iprange:

IP ranges
~~~~~~~~~

.. automodule:: geoip.models
   :members: Range


Backends
--------

There is currently no infrastructure to use alternative geoip backends,
but it's planned for future releases. Pull requests are also welcome.

Ipgeobase backend
~~~~~~~~~~~~~~~~~

`ipgeobase.ru <http://ipgeobase.ru>`_ is a database of Russian
and Ukranian IP networks mapped to geographical locations.

It's maintained by `RuCenter <http://nic.ru>`_ and updated daily.

As of 11 Nov 2013 it contains info on 992 cities and 152333 Ip Ranges
(some networks doesn't belong to CIS).

Here a is demo of ip detection: http://ipgeobase.ru/
