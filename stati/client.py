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
import logging
import json
import datetime
import time
import redis
from random import randint


logger = logging.getLogger('stati')


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
             "value": value,
             "random": time.time()})

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
        self._key = None
        self._channel = None
        self._connection_pool = None
        self._redis = None

    @property
    def channel(self):
        """Make channel name
        """
        if not self._channel:
            self._channel = "gottwall:{0}:{1}:{2}".format(self._project, self._public_key, self._private_key)
        return self._channel

    @property
    def data_key(self):
        """Make key that store
        """
        if not self._key:
            self._key = "gottwall:{0}:{1}".format(self._project, self._public_key, self._private_key)
        return self._key

    @property
    def redis(self):
        if not self._connection_pool:
            self._connection_pool = redis.ConnectionPool(host=self._host, port=self._port,
                                                     db=self._db, password=self._password)
        if not self._redis:
            self._redis = redis.Redis(connection_pool=self._connection_pool)

        return self._redis

    def incr(self, name, timestamp=None, value=1, filters={}):
        timestamp = timestamp or datetime.datetime.now()
        try:
            redis = self.redis

            redis.sadd(self.data_key, self.serialize(name, timestamp, value, filters))
            redis.publish(self.channel, json.dumps({"type": "notification"}))
        except Exception, e:
            print(e)
            logger.warn(e)

    def serialize(self, name, timestamp, value, filters={}):
        """Make data bucket

        :param data: dict of data
        """
        return json.dumps(
            {"name": name,
             "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
             "filters": filters,
             "value": value,
             "random": "{0}{1}".format(time.time(), str(randint(1, 1000)))})

