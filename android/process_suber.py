# -*- coding:utf-8 -*-
import datetime
import time
import re
import sys
sys.path.append("../")  # 为了引入instance
from instance import mongo_instance  # weixindb
from bson.objectid import ObjectId
import redis
r = redis.Redis()


def suber_entry(android_queue):
    suber(android_queue)

def suber(android_queue):
    suber = r.pubsub()
    suber.subscribe('there_is_a_task')
    for item in suber.listen():
        # print(item)
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        if item['type'] == 'message':
            data = item['data'].decode()
            print('- {} 接收到了来自公众号任务的分发，消息内容: {}'.format(t, data))
            pat = re.compile('__taskid_(.*)?')
            str_id = pat.findall(data, pos=0)[0]
            obj_id = ObjectId(str_id)
            # ANCHOR 查询task
            task = mongo_instance.tasks.find_one(filter={"_id": obj_id})
            print('- {} 根据 {} 查询到了该任务: '.format(t, str_id))
            print(task)
            tasks = android_queue.pickAll()
            # ANCHOR 检测重复
            # 如果公众号没有被添加过才需要添加
            for task_item in tasks:
                if task['task_biz_enname'] == task_item['task_biz_enname']:
                    print('- {} 公众号 {} 已存在队列中！ 无需再次添加！: '.format(t,
                                                              task_item['task_biz_enname']))
                    return

            # ANCHOR 检测未完成
            # 如果任务是未完成的状态 才加入队列
            if task['task_status'] == 'generate':
                # ANCHOR 加入队列
                android_queue.addItem(task)
                print('- {} 任务添加成功!'.format(t))

