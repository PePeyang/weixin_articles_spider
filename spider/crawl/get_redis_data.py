import re
import logging
import datetime
from http.cookies import SimpleCookie
from http import cookiejar
import urllib.parse as urlparse
from tools import replace_at_index
from instance import redis_instance, db_instance
from db.operate import TaskOperate

from items.home_request import FakeHomeParams
from items.list_request import FakeLoadParams

def drop_data_from_redis():
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
            redis_instance.delete(icon)

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
            redis_instance.delete(msg)

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
    # 还要刷新一次才有cookie
    # print(cookies)
    # biz = urlparse.parse_qs(data['REQUEST_URL'].split('?')[1])['__biz'][0]
    FakeHomeParams.cookies['wxuin'] = cookies['wxuin']
    # FakeHomeParams.cookies['version'] = cookies['version'] # version 应该有但是cookie转换后就是没有
    FakeHomeParams.cookies['pass_ticket'] = cookies['pass_ticket'] or ''
    FakeHomeParams.cookies['wap_sid2'] = cookies['wap_sid2']
    FakeHomeParams.params = replace_at_index(
        FakeHomeParams.params, 8, ('pass_ticket', cookies['pass_ticket']))



def _build_home_request_2(data):
    # print(data)
    try:
        FakeHomeParams.headers['x-wechat-uin'] = data['REQUEST_HEADERS']['X-WECHAT-UIN']
        FakeHomeParams.headers['x-wechat-key'] = data['REQUEST_HEADERS']['X-WECHAT-KEY']
    except Exception as err:
        print('无 x-wechat-key 和 x-wechat-uin')
        print(err)


    req_data = urlparse.parse_qs(data['REQUEST_DATA'])
    biz = req_data['__biz'][0]
    FakeHomeParams.params = replace_at_index(
        FakeHomeParams.params, 1, ('__biz', biz))

    # 不放心 再弄一次
    if req_data['pass_ticket']:
        print('这里果然有！')
        print(req_data['pass_ticket'])
        FakeHomeParams.cookies['pass_ticket'] = req_data['pass_ticket'][0]
        FakeLoadParams.cookies['pass_ticket'] = req_data['pass_ticket'][0]
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 9, ('pass_ticket', req_data['pass_ticket'][0]))

    cookie = SimpleCookie()
    cookie.load(data['REQUEST_COOKIE'])
    cookies = {}
    cookies = {i.key: i.value for i in cookie.values()}
    print(' --- _build_home_request_2 ---')
    print(cookies)

    try:
        cookies['wap_sid2']
        cookies['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = cookies['wap_sid2']
        FakeLoadParams.cookies['pass_ticket'] = cookies['pass_ticket']
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 9, ('pass_ticket', cookies['pass_ticket']))
    except Exception as err:
        pass




def tidy_data(rqlist, data):
    tidy_data_operate = TaskOperate('tidy_data_operate')
    now_time_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

    for biz, obj in data.items():
        # print(biz)
        l_in_db = tidy_data_operate.get_l_in_mongo(biz) or {}
        # print(type(l_in_db)) dict
        # print(l_in_db)
        icon_data = obj['geticon']
        msg_data = obj['getappmsgext']
        # print(icon_data)
        # print(msg_data)
        _build_home_request_1(eval(icon_data))
        _build_home_request_2(eval(msg_data))

        if not l_in_db:
            # 如果这是一个新的公众号
            l_in_db['update_time'] = now_time_str
            l_in_db['create_time'] = now_time_str
            l_in_db['Host'] = FakeHomeParams.headers['Host']
            l_in_db['User-Agent'] = FakeHomeParams.headers['User-Agent']
            l_in_db['biz'] = biz
            l_in_db['update_count'] = 1
            # l_in_db['bizname'] = bizname
            l_in_db['total_processed'] = 0

            l_in_db['start_index'] = 0
            l_in_db['end_index'] = 0
            l_in_db['start_article'] = ''
            l_in_db['end_article'] = ''
            tidy_data_operate.insert_l_in_mongo(l_in_db)
            pass
        else:
            # 如果数据库中已经有了这个公众号
            l_in_db['update_time'] = now_time_str
            l_in_db['User-Agent'] = FakeHomeParams.headers['User-Agent']

        rqlist.addItem(l_in_db)
    return rqlist
