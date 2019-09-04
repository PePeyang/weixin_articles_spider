# -*- coding:utf-8 -*-
from bson.objectid import ObjectId
import redis
import datetime
import time
import sys
import re
from phone.GZHCrawler import GZHCrawler
sys.path.append("../")  # 为了引入instance
from instance import mongo_instance  # weixindb
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def adb_entry(android_queue):
    # 每隔一分钟去队列检查下是否有任务在running 没有的话就搞一个变成running

    while True:
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        # TODO 这里貌似有点问题 但又不是逻辑问题 tasks
        is_empty_tasks = android_queue.isEmpty()

        if is_empty_tasks:
            print('- {} 没有任何可用任务'.format(t))
        else:
            for key in r.scan_iter("__running_task_"):
                value = r.get('__running_task_')
                running_taskid = value.split(
                    '_between_')[0]
                running_bizenname = value.split(
                    '_between_')[1]
                # 从数据库取得任务
                running_task = get_task_in_mongodb(ObjectId(running_taskid))
                if 'end_' in running_task['task_status']:
                    r.delete('__running_task_')
                elif 'running' in running_task['task_status']:
                    print('- {} 已经有运行中的任务了哦 _id是 {} bizename是 {} '.format(t,
                                                                          running_taskid, running_bizenname))

                break # NOTE 我曹!
            else:
                print('- {} 即将添加任务至安卓运行队列'.format(t))
                # 如果没有任何进行中的任务
                # 1. 将第一个任务设为进行中 存入数据库
                # 2. 通知代理，你有活要干啦！ 并且删除他
                try:
                    new_task = android_queue.popItem()
                    print('- {} 即将开始安卓任务'.format(t))
                    set_task_running(new_task)
                    print('- {} 即将开始插入mongodb'.format(t))
                    set_task_in_mongo(str(new_task['_id']))
                    print('- {} 即将开始插入redis'.format(t))
                    set_task_in_redis(
                        str(new_task['_id']), str(new_task['task_biz_enname']))
                    # print('- {} 即将通知anyproxy'.format(t))
                    # notify_http_proxy(str(new_task['_id']))
                    print('- {} 即将开始做adb操作'.format(t))

                    # TODO adb操作
                    gc = GZHCrawler(str(new_task['task_biz_enname']))
                    gc.run()

                except Exception as e:
                    print(' - 31行 这里出错了')
                    print(e)

        time.sleep(20)


# def pick_running(android_queue, tasks):
#     running_tasks = []
#     for task in tasks:
#         # 同一时间只能有一个running的
#         if task['task_status'] == 'running':
#             running_tasks.append(task)
#             break
#     return running_tasks


def get_task_in_mongodb(task_obj_id):
    return mongo_instance.tasks.find_one(filter={'_id': task_obj_id})

def set_task_running(task):
    task['task_status'] = 'running'

def set_task_in_mongo(taskid):
    task_obj_id = ObjectId(taskid)
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    mongo_instance.tasks.find_and_modify(
        query={'_id': task_obj_id}, update={'$set': {'task_status': 'running', 'task_updatetime': t}})

def set_task_in_redis(taskid, enname):
    # redis的key过期事件在获返回结果时是 key的值，所以在做相关任务时，可以把key名写成需要执行的函数名等等
    # 先清空
    for key in r.scan_iter("__running_task_"):
        r.delete(key)

    # r.set('__running_task_', '{}_between_{}'.format(
    #     taskid, enname), ex=60*10)  # TODO 重新整理下 那些redis的发布订阅监听
    r.set('__running_task_', '{}_between_{}'.format(taskid, enname))
    # NOTE  !!! 我曹
    r.set('which_task_should_be_timeout', taskid)

# def notify_http_proxy(taskid):
#     r.publish('there_is_a_adb', '__taskid_' + str(taskid))



