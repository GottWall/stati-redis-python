#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stati.client
~~~~~~~~~~~~

Client for GottWall

:copyright: (c) 2012 by GottWall team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/stati-python
"""

import simplejson as json
import datetime
import redis

class Client(object):
    """Base client
    """
    def __init__(self, project, private_key, public_key):
        self._project = project
        self._private_key = private_key
        self._public_key = public_key

    def serialize(self, name, timestamp, value, filters={}):
        """Make data bucket

        :param data: dict of data
        """
        return json.dumps(
            {"name": name,
             "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
             "filters": filters,
             "value": value})

    def incr(self, name, timestamp=datetime.datetime.now(), value=1,
             filters={}):
        """Add data incrementation

        :param name:
        :param timestamp:
        :param value:
        :param filters:
        """
        raise NotImplementedError


class RedisClient(Client):
    """GottWall client that send data to redis pub/sub
    """

    def __init__(self, project, private_key, public_key,
                 host='localhost', port=6379, password=None,
                 db=0):
        super(RedisClient, self).__init__(project, private_key, public_key)
        self._host = host
        self._port = port
        self._password = password
        self._db = db
        self._pool = None

    @property
    def channel(self):
        """Make channel name
        """
        return "gottwall:{0}:{1}:{2}".format(self._project, self._public_key, self._private_key)

    def incr(self, name, timestamp=datetime.datetime.now(), value=1,
             filters={}):
        pool = redis.ConnectionPool(host=self._host, port=self._port,
                                    db=self._db, password=self._password)
        r = redis.Redis(connection_pool=pool)

        r.publish(self.channel, self.serialize(name, timestamp, value, filters))

