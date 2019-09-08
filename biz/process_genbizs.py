# -*- coding:utf-8 -*-
import time
import datetime
import sys
import os
sys.path.append("../")
from bson.objectid import ObjectId
from instance.main_instance import mongo_instance, redis_instance  # weixindb
from tools.data_queue import Redis_queue

tasks_queue = Redis_queue('TASKS_QUEUE')

# 一次性从fakenames取出所有的biz
# 构造task数据
# 存入mongodb 发往android
# FIXME 找到bug原因
# print('- {} 找到了bizs {}'.format(bizs_time, str(list(bizs))))

def entry():
    initBizs()
    bizs = find_bizs()
    bizs_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    # type(bizs) <class 'pymongo.cursor.Cursor'>
    print('- {} 找到了bizs'.format(bizs_time))
    # tasks = build_task(list(bizs), 'new', None, 30 , 0)
    tasks = build_task(list(bizs[::]), 'count', 10, None, 0)
    # tasks = build_task(list(bizs), 'all', None, None, 0)
    mongo_instance.biznames.remove()
    tasks_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} 构造了tasks'.format(tasks_time))

def find_bizs():
    biznames = mongo_instance.biznames.find()
    return biznames
    # Raises: class: TypeError if any of the arguments are of improper type.
    # Returns an instance of: class: ~pymongo.cursor.Cursor corresponding to this query.

def build_task(bizs, task_mode, task_crawl_count, task_crawl_min, task_depth):
    tasks = []
    for biz in bizs:
        task = {}
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print('- {} idx: {} biz: {}'.format(t, 0, str(biz)))
        task['task_from'] = 'handle'
        task['task_biz_id'] = biz['_id']
        task['task_biz_enname'] = biz['fakename']
        task['task_biz_chname'] = biz['chname']
        task['task_createtime'] = t
        task['task_updatetime'] = t
        # generated running end_success end_fail end_timeout null
        # generated 任务生成
        # actived 加入running
        # running_in_adb 在手机上运行中
        # running_in_http 在proxy上运行中
        # running_in_scrapy 在爬虫上运行中
        # end_siccess 在手机上运行中
        task['task_status'] = 'generated'
        task['task_starttime'] = None
        task['task_endtime'] = None
        task['task_weight'] = 1
        task['task_mode'] = task_mode
        task['task_crawl_count'] = task_crawl_count
        task['task_crawl_min'] = task_crawl_min
        task['task_depth'] = task_depth  # html 0 html+imgs 1 html+comment 2
        task['task_start_loadid'] = None
        task['task_end_loadid'] = None

        # ANCHOR task插入mongodb
        taskid = str(insert_task(task).inserted_id)
        # ANCHOR task加入redis queue
        tasks_queue.addItem(taskid)
        # taskid == <class 'bson.objectid.ObjectId'>
        # notify_android(taskid)
        tasks.append(taskid)
        time.sleep(0.5)
    return tasks

def initBizs():
    fakenames = mongo_instance.biznames
    base_dir = os.path.dirname(__file__)
    ac = os.path.join(base_dir, '../', 'assets/fakenames.conf')
    print(ac)
    idx = 0
    if os.path.isfile(ac):
        with open(ac, 'rt', encoding='utf-8-sig') as fi:
            line = fi.readline()
            while line:
                idx += 1
                arr = line.strip().split(' ')
                # print(arr)
                fakename = {
                    'fakename': arr[0],
                    'chname': arr[1]
                }
                fakenames.insert_one(fakename)
                line = fi.readline()

def insert_task(task):
    return mongo_instance.tasks.insert_one(task)
    # An instance of :class:`~pymongo.results.InsertOneResult`

def notify_android(taskid):
    # ObjectId(taskid)
    redis_instance.publish('there_is_a_task', '__taskid_' + str(taskid))
