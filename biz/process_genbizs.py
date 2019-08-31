import sys
sys.path.append("../")  # 为了引入instance
from  instance import mongo_instance  # weixindb
import time
import datetime
from bson.objectid import ObjectId
import redis
r = redis.Redis()

# 一次性从fakenames取出所有的biz
# 构造task数据
# 存入mongodb 发往android


# FIXME 找到bug原因
# print('- {} 找到了bizs {}'.format(bizs_time, str(list(bizs))))


def entry():
    # ANCHOR
    bizs = find_bizs()
    bizs_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    # type(bizs) <class 'pymongo.cursor.Cursor'>
    print('- {} 找到了bizs'.format(bizs_time))
    # ANCHOR
    tasks = build_task(list(bizs), 'new', 30 , 0)
    tasks_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} 构造了tasks'.format(tasks_time))
    print(tasks)

def find_bizs():
    return mongo_instance.biznames.find()
    # Raises: class: TypeError if any of the arguments are of improper type.
    # Returns an instance of: class: ~pymongo.cursor.Cursor corresponding to this query.


def build_task(bizs, task_mode, task_crawlcount, task_depth):
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
        task['task_status'] = 'generate' #  generate running end_success end_fail
        task['task_starttime'] = None
        task['task_endtime'] = None
        task['task_weight'] = 1
        task['task_mode'] = task_mode
        task['task_crawlcount'] = task_crawlcount
        task['task_start_articleid'] = None
        task['task_end_articleid'] = None
        task['task_depth'] = task_depth  # html 0 html+imgs 1 html+comment 2
        # ANCHOR
        taskid = insert_task(task).inserted_id
        # taskid == <class 'bson.objectid.ObjectId'>
        # ANCHOR
        notify_android(taskid)
        tasks.append(taskid)
        time.sleep(1)

    return tasks

def insert_task(task):
    return mongo_instance.tasks.insert_one(task)
    # An instance of :class:`~pymongo.results.InsertOneResult`


def notify_android(taskid):
    # ObjectId(taskid)
    r.publish('there_is_a_task', '__taskid_' + str(taskid))
