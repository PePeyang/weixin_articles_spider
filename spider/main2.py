# 构造home请求获取 appmsg_token
# 构造分页请求
#
# from new_tools.data_queue import RQ
from instance import redis_instance
import json
import re
from time import time
import datetime as d
import requests
from http.cookies import SimpleCookie
from http import cookiejar
import urllib.parse as urlparse

class Fakehomeparams:
    cookies = {
        'rewardsn': '',
        'wxuin': '3604431997',
        'devicetype': 'android-23',
        'version': '27000634',
        'lang': 'zh_CN',
        'pass_ticket': '',
        'wap_sid2': '',
        'wxtokenkey': '777',
    }

    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MMWEBID/736 MicroMessenger/7.0.6.1460(0x27000634) Process/toolsmp NetType/WIFI Language/zh_CN',
        'x-wechat-uin': '',
        'x-wechat-key': '',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.tencent.mm',
    }

    params = (
        ('action', 'home'),
        ('__biz', ''),
        ('devicetype', 'android-23'),
        ('version', '27000634'),
        ('lang', 'zh_CN'),
        ('nettype', 'WIFI'),
        ('a8scene', '7'),
        ('session_us', 'gh_9e26999263b5'),
        ('pass_ticket', ''),
        ('wx_header', '1'),
    )


class Fakeloadparams:
    cookies = {
        'rewardsn': '',
        'wxtokenkey': '777',
        'wxuin': '3604431997',
        'devicetype': 'android-23',
        'version': '27000634',
        'lang': 'zh_CN',
        'pass_ticket': '',
        'wap_sid2': '',
    }

    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 MMWEBID/736 MicroMessenger/7.0.6.1460(0x27000634) Process/toolsmp NetType/WIFI Language/zh_CN',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': '*/*',
        # 'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzUyMzkwNTQzNQ==&devicetype=android-23&version=27000634&lang=zh_CN&nettype=WIFI&a8scene=7&session_us=gh_9e26999263b5&pass_ticket=%2FwVUpAEtgoBvTouSB3nRI5qyK6t2sGFiihU0qj8IjUsCRWbJixaNVyZ7%2FeO0iFjG&wx_header=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
    }

    params = (
        ('action', 'getmsg'),
        ('__biz', 'MzUyMzkwNTQzNQ=='),
        ('f', 'json'),
        ('offset', '14'),
        ('count', '10'),
        ('is_ok', '1'),
        ('scene', ''),
        ('uin', '777'),
        ('key', '777'),
        ('pass_ticket', ''),
        ('wxtoken', ''),
        ('appmsg_token', ''),
        ('x5', '0'),
    )

class NORMAL_URLS:
    home = "https://mp.weixin.qq.com/mp/profile_ext?action=home"
    getmsg = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg"
    article = "https://mp.weixin.qq.com/s?"

def replace_at_index(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)

def tup_to_query(url, tup):
    # lst = list(tup)
    for i in range(len(tup)):
        pass
        # key_and_value = tup[0] + '=' + str(tup[1])
        # print(key_and_value)


def send_request():
    response = requests.get('https://mp.weixin.qq.com/mp/profile_ext',
                        headers=Fakehomeparams.headers, params=Fakehomeparams.params, cookies=Fakehomeparams.cookies)
    if response.content.decode().find('失效的验证页面') > 0:
        print('失效的验证页面')
    else:
        login_cookies = requests.utils.dict_from_cookiejar(response.cookies)
        print(login_cookies['wap_sid2'])
        print(login_cookies['pass_ticket'])
        Fakeloadparams.cookies['pass_ticket'] = login_cookies['pass_ticket']
        Fakeloadparams.cookies['wap_sid2'] = login_cookies['wap_sid2']
        Fakeloadparams.params = replace_at_index(
            Fakeloadparams.params, 9, ('pass_ticket', login_cookies['pass_ticket']))
        return response.content.decode()




def build_home_request_1(data):
    # print(data)
    cookie = SimpleCookie()
    cookie.load(data['REQUEST_COOKIE'])
    cookies = {}
    cookies = {i.key: i.value for i in cookie.values()}
    Fakehomeparams.cookies['wxuin'] = cookies['wxuin']
    # Fakehomeparams.cookies['version'] = cookies['version']
    Fakehomeparams.cookies['pass_ticket'] = cookies['pass_ticket']
    Fakehomeparams.cookies['wap_sid2'] = cookies['wap_sid2']
    Fakehomeparams.params = replace_at_index(
        Fakehomeparams.params, 8, ('pass_ticket', cookies['pass_ticket']))

def build_home_request_2(data):
    # print(data)
    Fakehomeparams.headers['x-wechat-uin'] = data['REQUEST_HEADERS']['X-WECHAT-UIN']
    Fakehomeparams.headers['x-wechat-key'] = data['REQUEST_HEADERS']['X-WECHAT-KEY']
    biz = urlparse.parse_qs(data['REQUEST_DATA'])['__biz'][0]
    # print(biz)
    Fakehomeparams.params = replace_at_index(
        Fakehomeparams.params, 1, ('__biz', biz))



def build_load_request(appmsg_token):
    print(appmsg_token)

    Fakeloadparams.params = replace_at_index(
        Fakeloadparams.params, 1, ('__biz', Fakehomeparams.params[1][1]))

    Fakeloadparams.params = replace_at_index(
        Fakeloadparams.params, 11, ('appmsg_token', appmsg_token))

    # print(Fakeloadparams.headers)
    print(Fakeloadparams.cookies)
    # print(Fakeloadparams.params)



def loop_request_load():
    import time
    print(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
    idx=0
    while True:
        response = requests.get(
            'https://mp.weixin.qq.com/mp/profile_ext',
            headers=Fakeloadparams.headers,
            params=Fakeloadparams.params,
            cookies=Fakeloadparams.cookies
        )
        try:
            idx+=1
            print(json.loads(response.text))
            print(idx)
            time.sleep(2)
        except Exception as identifier:
            print(identifier)
            print(idx)
            print(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))




if __name__ == '__main__':
    print('__main__')
    # MzIzNjMzMTgyNw==_REQUEST
    # 一组一组拿出来
    keys = redis_instance.keys('*_REQUEST')
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
    # print(str(time()))
    content = send_request()
    if not content:
        content = ''

    pat = re.compile(r'window.appmsg_token = "(.*?)"')
    appmsg_tokens = pat.findall(content, pos=0)
    for m in appmsg_tokens:
        build_load_request(m)
        loop_request_load()




