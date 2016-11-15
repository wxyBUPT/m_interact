#coding=utf-8
__author__ = 'xiyuanbupt'
# e-mail : xywbupt@gmail.com

import redis

from conf_util import ConfUtil

redis_pool = redis.ConnectionPool(
    host = ConfUtil.getRedisHost(),
    port = ConfUtil.getRedisPort(),
    db = ConfUtil.getRedisDb()
)