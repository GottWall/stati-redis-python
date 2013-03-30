#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stati_redis.example
~~~~~~~~~~~~~

Stati example to use Redis pub/sub transport

:copyright: (c) 2012 by GottWall team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
:github: http://github.com/GottWall/stati-redis-python
"""

from stati_redis import RedisClient

private_key = "gottwall_privatekey"
public_key = "project_public_key"
project = "test_gottwall_project"

host = "10.8.9.8"

cli = RedisClient(
    private_key=private_key,
    public_key=public_key,
    project=project, db=2,
    host=host)

cli.incr(metric="orders", value=2, filters={"current_status": "Completed"})
