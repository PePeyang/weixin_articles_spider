# 构造home请求获取 appmsg_token
# 构造分页请求
#
from tools.load_list_parse import list_into_dbdata, list_parse
from phone.operate import Operate
from instance import redis_instance, db_instance, db_loadlist
import json
import re
from time import time
import datetime as d
import requests
from http.cookies import SimpleCookie
from http import cookiejar
import urllib.parse as urlparse


# def save_list_to_db(list_db):
#     # TODO fix
#     db_loadlist.insert_many(list_db)
#     pass

# def loop_request_load():
#     import time
#     print(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
#     idx=0
#     items_len=0
#     offset=0
#     # return
#     # 循环机制改变一下 需要捕捉到所有的真实错误
#     # ANCHOR 测试结果 一天最多请求 1000次
#     while True:
#         try:
#             try:
#                 response = requests.get(
#                     'https://mp.weixin.qq.com/mp/profile_ext',
#                     headers=Fakeloadparams.headers,
#                     params=Fakeloadparams.params,
#                     cookies=Fakeloadparams.cookies
#                 )
#             except Exception as request_err:
#                 print(request_err)
#                 raise Exception('HUMAN_ERROR: 请求出错了')

#             idx+=1
#             offset+=10

#             Fakeloadparams.params = replace_at_index(
#                 Fakeloadparams.params, 3, ('offset', offset))

#             list_parse_res = list_parse(eval(response.text))
#             print(type(list_parse_res))
#             if type(list_parse_res['ret']) == type(0):
#                 print(list_parse_res)
#                 raise Exception('HUMAN_ERROR: 这条数据parse失败了')
#             list_db_data = list_into_dbdata(list_parse_res)
#             if not list_db_data:
#                 raise Exception('HUMAN_ERROR: 后面无数据了')

#             try:
#                 save_list_to_db(list_db_data)
#             except Exception as db_err:
#                 print(db_err)
#                 raise Exception('HUMAN_ERROR: 数据库插入出错了')
#             items_len += len(list_db_data)
#             print('成功处理第 {} 个load请求，当前 offset= {} items_len= {}'.format(
#                 idx, offset, items_len))
#             time.sleep(3)
#         except Exception as err:
#             print('失败处理第 {} 个load请求，当前 offset= {} items_len= {}'.format(
#                 idx, offset, items_len))
#             print(err)
#             if str(err).find('无数据') > 0:
#                 break
#     print(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))


def operate_phone(client):
    client.home_click()
    # client.search_text()
    # client.tab_click()
    # client.enter_into_gzh()


if __name__ == '__main__':
    print('__main__')

    from crawl.get_redis_data import get_data_from_redis, tidy_data
    from crawl.process_spider import listSpider

    data = get_data_from_redis()
    rqlist = tidy_data(data)
    print(' --- rqlist --- ')
    print(rqlist)


    while not rqlist.isEmpty():
        rq = rqlist.popItem()
        # print(rq)
        lspider = listSpider(rq)
        lspider.start()


    # client = Operate('苏州青舞舞蹈艺术')
    # operate_phone(client)

    # content = send_request()
    # if not content:
    #     print('无效content')
    #     content = ''


    # if content.find('操作频繁') > 0:
    #     print('HUMAN_ERROR: 操作频繁 限制24小时 请更换微信')


    # pat = re.compile(r'window.appmsg_token = "(.*?)"')
    # appmsg_tokens = pat.findall(content, pos=0)

    # for m in appmsg_tokens:
    #     build_load_request(m)
    #     loop_request_load()




