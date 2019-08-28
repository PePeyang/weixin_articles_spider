import re
import logging
import datetime
from http.cookies import SimpleCookie
from http import cookiejar
import urllib.parse as urlparse
from tools import replace_at_index
from tools.data_queue import RQ
from instance import redis_instance, db_instance
from db.operate import Operate as DB_OPERATE
# DB_OPERATE insert_l_in_mongo, get_l_in_mongo, update_l_in_mongo
from items.home_request import FakeHomeParams
from items.list_request import FakeLoadParams

def get_data_from_redis():
    icons = redis_instance.keys('__fake_geticon*_REQUEST')
    msgs = redis_instance.keys('__fake_getappmsgext*_REQUEST')
    data = {}
    pat1 = re.compile("__fake_geticon_biz=(.*?)_REQUEST")
    pat2 = re.compile("__fake_getappmsgext_biz=(.*?)_REQUEST")

    try:
        for icon in icons:
            # print(icon)
            biz = pat1.findall(icon.decode(), pos=0)[0]
            # print(biz)
            # continue
            data[biz] = {}
            data[biz]['geticon'] = redis_instance.get(icon).decode()

        for msg in msgs:
            # print(msg)
            biz = pat2.findall(msg.decode(), pos=0)[0]
            # print(biz)
            # continue
            if data[biz]['geticon']:
                data[biz]['getappmsgext'] = redis_instance.get(msg).decode()
            else:
                data[biz] = {}
                data[biz]['getappmsgext'] = redis_instance.get(msg).decode()
    except Exception as err:
        logging.error(err)
        logging.info('请检查redis数据')

    # print(data)
    return data

def _build_home_request_1(data):
    # print(data)
    cookie = SimpleCookie()
    cookie.load(data['REQUEST_COOKIE'])
    cookies = {}
    cookies = {i.key: i.value for i in cookie.values()}
    print(cookies)
    FakeHomeParams.cookies['wxuin'] = cookies['wxuin']
    # FakeHomeParams.cookies['version'] = cookies['version']
    FakeHomeParams.cookies['pass_ticket'] = cookies['pass_ticket']
    FakeHomeParams.cookies['wap_sid2'] = cookies['wap_sid2']
    FakeHomeParams.params = replace_at_index(
        FakeHomeParams.params, 8, ('pass_ticket', cookies['pass_ticket']))



def _build_home_request_2(data):
    # print(data)
    FakeHomeParams.headers['x-wechat-uin'] = data['REQUEST_HEADERS']['X-WECHAT-UIN']
    FakeHomeParams.headers['x-wechat-key'] = data['REQUEST_HEADERS']['X-WECHAT-KEY']
    biz = urlparse.parse_qs(data['REQUEST_DATA'])['__biz'][0]
    print('X-WECHAT-UIN=' + data['REQUEST_HEADERS']['X-WECHAT-UIN'])
    print('X-WECHAT-KEY=' + data['REQUEST_HEADERS']['X-WECHAT-KEY'])
    print('biz=' + biz)
    FakeHomeParams.params = replace_at_index(
        FakeHomeParams.params, 1, ('__biz', biz))


def tidy_data(data):
    tidy_data_operate = DB_OPERATE('tidy_data_operate')
    l = list()
    now_time_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

    for biz, obj in data.items():
        l_in_db = tidy_data_operate.get_l_in_mongo(biz) or {}
        l_in_db['update_time'] = now_time_str
        icon_data = obj['geticon']
        msg_data = obj['getappmsgext']
        # print(icon_data)
        # print(msg_data)
        _build_home_request_1(eval(icon_data))
        _build_home_request_2(eval(msg_data))

        if not l_in_db:
            # 如果这是一个新的公众号
            l_in_db['create_time'] = now_time_str
            tidy_data_operate.insert_l_in_mongo(biz)
            pass
        else:
            # 如果数据库中已经有了这个公众号
            tidy_data_operate.update_l_in_mongo(biz)

    return None
