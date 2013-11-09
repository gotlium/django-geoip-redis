# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='django-geoip-redis',
    version="1.0.1",
    description='Django GeoIP. Based on default DB or Redis.',
    keywords='django geoip mysql redis',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Proxy Servers',
    ],
    author="GoTLiuM InSPiRiT",
    author_email='gotlium@gmail.com',
    url='https://github.com/gotlium/django-geoip-redis',
    license='GPL v3',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'redis>=2.8.0',
        'hiredis>=0.1.1',
        'ipaddress>=1.0.6',
        'progressbar>=2.3',
        'django-celery>=3.0.23',
    ]
)
