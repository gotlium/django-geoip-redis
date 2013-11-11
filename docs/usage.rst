Usage
=====

The app provides both high and low-level APIs to work with geolocation.
Low-level API works super-simple: it guesses geographic location by an IP adress.
High-level API is more complex and deeply integrated in Django: it automatically
detects user location in every request and makes it available as ``request.geo``.

.. _lowlevel:

Low-level API usage
-------------------

Low-level API allows you to guess user's location by his IP address.
This function returns dictionary associated with IP's city, area, country, isp
and provider.

Here is a basic example::

  from geoip import record_by_ip_as_dict

  ip = '91.195.136.52'

  geoip_record = record_by_ip_as_dict(ip)

  if geoip_record is not None:
      print geoip_record.get('country')
      print geoip_record.get('area')
      print geoip_record.get('city')
      print geoip_record.get('isp')
      print geoip_record.get('provider')
  else:
      print 'Unknown location'

.. _highlevel:

High-level API usage
--------------------

The app provides a convenient way to detect user location automatically.
If you've followed :ref:`advanced installation instructions <advanced>`,
user's location should be accessible via ``request`` object::

    def my_view(request):
        """ Passing location into template """
        ...
        context['geo'] = request.geo
        ...

