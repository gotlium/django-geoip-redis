django-geoip-redis
==================

App to figure out where your visitors are from by their IP address.

Detects country, region, city, isp, provider and netspeed querying in the database with geodata. |br|
Optional :ref:`high-level API <highlevel>` provides geo data on request object.

.. note::
    Current version support only `ipgeobase.ru <http://ipgeobase.ru>`_.
    IPGeoBase provide information about Russia and Ukraine.
    But you can import MaxMind databases manually, if you have subscription.


Contents
--------

.. toctree::
  :maxdepth: 1

  installation
  usage
  howitworks
  update
  settings
  contributing
  changelog
  authors
  performance
  dev_install
  why_dgr


Contributing
------------

You can grab latest code on ``development`` branch at Github_.

Feel free to submit issues_, pull requests are also welcome.

Good contributions follow :ref:`simple guidelines <contributing>`

.. _Github: https://github.com/gotlium/django-geoip-redis
.. _issues: https://github.com/gotlium/django-geoip-redis/issues

.. |br| raw:: html

   <br />

