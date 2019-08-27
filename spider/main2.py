# 构造home请求获取 appmsg_token
# 构造分页请求
#
# from new_tools.data_queue import RQ
from instance import redis_instance
import json
import requests
from http.cookies import SimpleCookie
import urllib.parse as urlparse

class FAKE_PARAMS:
    cookies = {
        'rewardsn': '',
        'wxuin': '3604431997',
        'devicetype': 'android-23',
        'version': '27000634',
        'lang': 'zh_CN',
        'pass_ticket': '/wVUpAEtgoBvTouSB3nRI5qyK6t2sGFiihU0qj8IjUsCRWbJixaNVyZ7/eO0iFjG',
        'wap_sid2': 'CP2I3bYNElxzblBQaWJmQk1MYjlTX1dlTEhOU3ltWlM2bk56Z0tTbEhYb25HTkN4NnJkVmpCZllVSnU1Z2xScGxjbkRQU2oxX1dpay1QVnFZbVNzSTludUlMNFZ1djhEQUFBfjCb/ZPrBTgNQAE=',
        'wxtokenkey': '777',
    }

    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MMWEBID/736 MicroMessenger/7.0.6.1460(0x27000634) Process/toolsmp NetType/WIFI Language/zh_CN',
        'x-wechat-uin': 'MzYwNDQzMTk5Nw%3D%3D',
        'x-wechat-key': '7ff0b5e01ac5510c9f0535551889c0cc0dd1e3747b94fdf29634fcae9095019513834ee1497f3c70cf16f97691c405f06650c366e4432737db063d4e03d7b696a2301ab28971b386cb2729f1ec4952e2',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.tencent.mm',
    }

    params = (
        ('action', 'home'),
        ('__biz', 'MzUyMzkwNTQzNQ=='),
        ('devicetype', 'android-23'),
        ('version', '27000634'),
        ('lang', 'zh_CN'),
        ('nettype', 'WIFI'),
        ('a8scene', '7'),
        ('session_us', 'gh_9e26999263b5'),
        ('pass_ticket', '/wVUpAEtgoBvTouSB3nRI5qyK6t2sGFiihU0qj8IjUsCRWbJixaNVyZ7/eO0iFjG'),
        ('wx_header', '1'),
    )


class NORMAL_URLS:
    home = "https://mp.weixin.qq.com/mp/profile_ext?action=home"
    getmsg = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg"
    article = "https://mp.weixin.qq.com/s?"

def replace_at_index(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)

def send_request():
    try:
        response = requests.get('https://mp.weixin.qq.com/mp/profile_ext',
                            headers=FAKE_PARAMS.headers, params=FAKE_PARAMS.params, cookies=FAKE_PARAMS.cookies)
        return response
    except Exception:
        return {'content': b""}

def build_home_request_1(data):
    # print(data)
    cookie = SimpleCookie()
    cookie.load(data['REQUEST_COOKIE'])
    cookies = {}
    cookies = {i.key: i.value for i in cookie.values()}
    FAKE_PARAMS.cookies['wxuin'] = cookies['wxuin']
    # FAKE_PARAMS.cookies['version'] = cookies['version']
    FAKE_PARAMS.cookies['pass_ticket'] = cookies['pass_ticket']
    FAKE_PARAMS.cookies['wap_sid2'] = cookies['wap_sid2']
    FAKE_PARAMS.params = replace_at_index(
        FAKE_PARAMS.params, 8, ('pass_ticket', cookies['pass_ticket']))

def build_home_request_2(data):
    # print(data)
    FAKE_PARAMS.headers['x-wechat-uin'] = data['REQUEST_HEADERS']['X-WECHAT-UIN']
    FAKE_PARAMS.headers['x-wechat-key'] = data['REQUEST_HEADERS']['X-WECHAT-KEY']
    biz = urlparse.parse_qs(data['REQUEST_DATA'])['__biz'][0]
    # print(biz)
    FAKE_PARAMS.params = replace_at_index(
        FAKE_PARAMS.params, 1, ('__biz', biz))

    print(FAKE_PARAMS().params)



if __name__ == '__main__':
    print('__main__')
    # MzIzNjMzMTgyNw==_REQUEST
    # 一组一组拿出来
    keys = redis_instance.keys('*MzIzNjMzMTgyNw==_REQUEST')
    geticon_key = str(keys[0], encoding="utf-8")
    getappmsgext_key = str(keys[1], encoding="utf-8")
    # print(geticon_key)
    # print(getappmsgext_key)
    geticon_value = redis_instance.get(geticon_key)
    getappmsgext_value = redis_instance.get(getappmsgext_key)
    geticon_value = json.loads(geticon_value.decode())
    getappmsgext_value = json.loads(getappmsgext_value.decode())
    # print(geticon_value)
    # print(getappmsgext_value
    build_home_request_1(geticon_value)
    build_home_request_2(getappmsgext_value)

    content = send_request().content.decode()
    print(content)



