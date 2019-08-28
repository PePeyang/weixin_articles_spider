import re
from new_tools.data_queue import RQ
from instance import redis_instance, db_instance

def get_data_from_redis():
    icons = redis_instance.keys('__fake_geticon*_REQUEST')
    msgs = redis_instance.keys('__fake_getappmsgext*_REQUEST')

    data = {}
    pat1 = re.compile("__fake_geticon_biz=(.*?)_REQUEST")
    pat2 = re.compile("__fake_getappmsgext_biz=(.*?)_REQUEST")

    for icon in icons:
        # print(icon)
        biz = pat1.findall(icon.decode(), pos=0)[0]
        print(biz)
        # continue
        data[biz] = {}
        data[biz]['geticon'] = redis_instance.get(icon).decode()

    for msg in msgs:
        # print(msg)
        biz = pat2.findall(msg.decode(), pos=0)[0]
        print(biz)
        # continue
        if data[biz]['geticon']:
            data[biz]['getappmsgext'] = redis_instance.get(msg).decode()
        else:
            data[biz] = {}
            data[biz]['getappmsgext'] = redis_instance.get(msg).decode()

    print(data)

