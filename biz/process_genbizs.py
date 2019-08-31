from instance import mongo_instance  # weixindb
import time
import datetime

# 一次性从fakenames取出所有的biz
# 构造task数据
# 存入mongodb 发往android

def entry():
    bizs = find_bizs()
    bizs_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} 找到的bizs {}'.format(bizs_time, str(bizs)[0::50]))

    tasks = build_task(bizs)
    tasks_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} 构造的tasks {}'.format(tasks_time, str(tasks)[0::50]))
    pass


def find_bizs():
    return mongo_instance.biznames.find({})


def build_task(bizs):
    tasks = []
    for biz,idx in bizs:
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print('- {} idx: {} biz: {}'.format(t, idx, biz))


        tasks.append()
        time.sleep(3)

    return tasks
