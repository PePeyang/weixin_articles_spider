import sys
sys.path.append("...")
from instance.main_instance import mongo_instance, redis_instance  # weixindb
import datetime
import re
import time
from bson.objectid import ObjectId
from tools.data_queue import Redis_queue
tasks_queue = Redis_queue('TASKS_QUEUE')

def listen_task_entry():
    # 每隔一分钟去队列检查下是否有任务在running 没有的话就搞一个变成actived

    while True:
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        is_empty_tasks = tasks_queue.isEmpty()
        # ANCHOR 判断task队列是否有内容
        if is_empty_tasks:
            pass
            print('- {} 没有任何可用任务'.format(t))
        else:
            running_taskid = redis_instance.get('__running_task_')

            if running_taskid:
                # ANCHOR redis中已有运行中的任务
                # 从数据库取得任务
                running_task = get_task_in_mongodb(running_taskid)
                running_bizenname = running_task['task_biz_enname']
                print('- {} 已经有运行中的任务了哦 _id是 {} bizename是 {} '.format(t,
                                                                        running_taskid, running_bizenname))
            else:
                # ANCHOR redis中没有运行中的任务
                # 拿出一条任务来执行
                print('- {} 添加任务至安卓运行队列'.format(t))
                running_taskid = tasks_queue.popItem()  # tasks_queue 不为空
                set_task_in_redis(running_taskid)
                set_task_mongodb_status(running_taskid, 'actived')

        time.sleep(10)


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

def set_task_in_redis(taskid):
    # redis的key过期事件在获返回结果时是 key的值，所以在做相关任务时，可以把key名写成需要执行的函数名等等
    # 先清空
    for key in redis_instance.scan_iter("__running_task_"):
        redis_instance.delete(key)

    redis_instance.set('__running_task_', '{}'.format(taskid))
    # NOTE  !!! 我曹
    redis_instance.set('which_task_should_be_timeout', taskid)
