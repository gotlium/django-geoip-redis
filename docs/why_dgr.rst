Why django-geoip-redis?
=======================

Advantages
----------
* For real-time projects and application
* ISP & Provider/Org support
* Native database is not used to detect geo data
* Do not depend to hosting or environments
* Very faster, compared with analogues with same capabilities
* GeoData will be detect once and stored on cookie
* Ability to get geo location on templates
* Ability to specify ranges for providers/org from the admin
* Update database from admin by one click
* Custom location data specified by user
* Relations with your apps


FAQ
----

Each time a page is requested - determined geo data?

* once, and geo data was stored on cookie

Why not Nginx or Apache with mod_geoip?

* maxmind geoip databases is not a free
* we can't change provider range on the fly or define custom data. or anything else.

Is it possible to convert maxmind database into Redis?

* yes. instruction stored on docs.
