import sys
sys.path.append("../")
from tools import replace_at_index
from config import FakeLoadParams
from config import FakeHomeParams

import urllib.parse as urlparse
from http import cookiejar
from http.cookies import SimpleCookie

from instance import mongo_instance  # weixindb
import redis
import datetime
import re
from bson.objectid import ObjectId
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def listen_http_entry():
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(' {} 开始 listen_http_entry...'.format(t))



def listen_http_entryDUP():
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    http = find_a_http_in_mongodb('313131313131313131313131')
    print(http)
    set_home_params_config_N1(http['geticon'])
    set_home_params_config_N2(http['getappmsgext'])

def find_a_http_in_mongodb(httpid):
    http_obj_id = ObjectId(httpid)
    return mongo_instance.https.find_one({'_id': http_obj_id})


def set_home_params_config_N1(data):
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
    FakeHomeParams.params['pass_ticket'] = cookies['pass_ticket']


def set_home_params_config_N2(data):
    # print(data)
    try:
        FakeHomeParams.headers['x-wechat-uin'] = data['REQUEST_HEADERS']['X-WECHAT-UIN']
        FakeHomeParams.headers['x-wechat-key'] = data['REQUEST_HEADERS']['X-WECHAT-KEY']
    except Exception as err:
        print('无 x-wechat-key 和 x-wechat-uin')
        print(err)

    req_data = urlparse.parse_qs(data['REQUEST_DATA'])
    FakeHomeParams.params['__biz'] = req_data['__biz'][0]
    # 不放心 再弄一次
    if req_data['pass_ticket']:
        print('这里果然有！')
        print(req_data['pass_ticket'])
        FakeHomeParams.cookies['pass_ticket'] = req_data['pass_ticket'][0]
        FakeLoadParams.cookies['pass_ticket'] = req_data['pass_ticket'][0]
        FakeLoadParams.params['pass_ticket'] = req_data['pass_ticket'][0]

    cookie = SimpleCookie()
    cookie.load(data['REQUEST_COOKIE'])
    cookies = {}
    cookies = {i.key: i.value for i in cookie.values()}
    print(' --- set_home_params_config_N2 ---')
    print(cookies)

    try:
        cookies['wap_sid2']
        cookies['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = cookies['wap_sid2']
        FakeLoadParams.cookies['pass_ticket'] = cookies['pass_ticket']
        FakeLoadParams.params['pass_ticket'] = cookies['pass_ticket']

    except Exception as err:
        pass


