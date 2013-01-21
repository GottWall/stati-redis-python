#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
stati
~~~~~~~~~~~~~~~~~~

Simple statistics aggregator


:copyright: (c) 2012 by GottWall team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

__all__ = 'get_version', 'Client', 'RedisClient'
__author__ = "Alex Lispython (alex@obout.ru)"
__license__ = "BSD, see LICENSE for more details"
__version_info__ = (0, 0, 4)
__build__ = 0x00004
__version__ = ".".join(map(str, __version_info__))
__maintainer__ = "Alexandr Lispython"


from stati.client import RedisClient, Client

assert RedisClient
assert Client


def get_version():
    return __version__
