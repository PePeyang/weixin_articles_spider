# -*- coding:utf-8 -*-
import datetime
import time
import sys
sys.path.append("../")  # 为了引入instance
from instance import mongo_instance  # weixindb
from bson.objectid import ObjectId
import redis
r = redis.Redis()


def suber_entry():
    suber()


def suber():
    suber = r.pubsub()
    suber.subscribe('there_is_a_task')
    for item in suber.listen():
        print(item)
