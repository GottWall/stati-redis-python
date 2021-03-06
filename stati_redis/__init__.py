#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
stati_redis
~~~~~~~~~~~~~~~~~~

Simple statistics aggregator


:copyright: (c) 2012 - 2013 by GottWall team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

__all__ = 'get_version', 'Client'
__author__ = "Alex Lispython (alex@obout.ru)"
__license__ = "BSD, see LICENSE for more details"
__maintainer__ = "Alexandr Lispython"

try:
    __version__ = __import__('pkg_resources') \
        .get_distribution('stati_redis').version
except Exception, e:
    __version__ = 'unknown'

if __version__ == 'unknown':
    __version_info__ = (0, 0, 0)
else:
    __version_info__ = __version__.split('.')
__build__ = 0x00005


from stati_redis.client import Client, RedisClient

assert Client
assert RedisClient


def get_version():
    return __version__
