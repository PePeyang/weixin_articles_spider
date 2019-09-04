# -*- coding:utf-8 -*-
from bson.objectid import ObjectId
import redis
import datetime
import time
import sys
import re
from phone.GZHCrawler import GZHCrawler
from instance import mongo_instance, redis_instance  # weixindb

def adb_entry():
    # 每隔一分钟去队列检查下是否有任务在running 没有的话就搞一个变成running

    while True:
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        running_taskid = redis_instance.get('__running_task_')
        if running_taskid:
            running_task = get_task_in_mongodb(running_taskid)
            running_bizenname = running_task['task_bizenname']
            running_status = running_task['task_status']

            if running_status == 'actived':
                print('- {} 即将开始改变状态'.format(t))
                set_task_mongodb_status(running_taskid, 'running_in_adb')

                print('- {} 即将开始做adb操作'.format(t))
                gc = GZHCrawler(str(running_bizenname))
                gc.run()

            else:
                pass
                print('- 您的当前运行中的任务状态为 %s' % running_status)

        else:
            pass


        time.sleep(62)

def get_task_in_mongodb(taskid):
    task_obj_id = ObjectId(taskid)
    return mongo_instance.tasks.find_one(filter={'_id': task_obj_id})

def set_task_mongodb_status(taskid, status):
    task_obj_id = ObjectId(taskid)
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    mongo_instance.tasks.find_and_modify(
        query={'_id': task_obj_id},
        update={'$set': {
            'task_status': status,
            'task_updatetime': t
        }})