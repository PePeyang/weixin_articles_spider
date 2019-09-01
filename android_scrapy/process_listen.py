# from instance import mongo_instance  # weixindb
import redis
import datetime
import re
from bson.objectid import ObjectId
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def listen_http_entry():
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(' {} 开始了对__keyspace@0__:__running_http_的订阅...'.format(t))
    suber = r.pubsub()
    suber.subscribe('__keyspace@0__:__running_http_')

    for item in suber.listen():
        print(' 监听到了事件')
        print(item)
        if item['type'] == 'message' and item['data'] == 'set':
            # __running_http_
            t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
            httpid = r.get('__running_http_')
            print(' {} 发现http数据 {}'.format(t, httpid))
            # biz_enname = value.split('_between_')[1]
            # print(' {} 时间到了任务过期: {} '.format(t, taskid))
            # # ANCHOR 设置task状态为过时
            # set_task_in_mongodb(ObjectId(taskid))


# def set_task_in_mongodb(task_obj_id):
#     t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
#     mongo_instance.tasks.find_and_modify(
#         query={'_id': task_obj_id}, update={'$set': {'task_status': 'end_timeout', 'task_updatetime': t}})



