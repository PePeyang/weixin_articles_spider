import datetime
import scrapy
import re
from ..items import HomeItem
from config import FakeLoadParams
from config import FakeHomeParams
from config import NORMAL_URLS
from scrapy.http import TextResponse
from bson.objectid import ObjectId
from instance import redis_instance, mongo_instance
from http.cookies import SimpleCookie


class LoadSpider(scrapy.Spider):
    name = 'LoadSpider'
    allowed_domains = ['mp.weixin.qq.com']
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(' - {} LoadSpider开始爬取了..'.format(t))
    custom_settings = {
        # redis
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
        'REDIS_DB': '0',
        # mongodb
        'MONGO_URL': 'mongodb://127.0.0.1:27017',
        'MONGO_DB': 'weixindb',
        # midlewares
        'ITEM_PIPELINES': {
            #
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'android_scrapy.homemiddlewares.HomeDownloaderMiddleware': 543,
        },
        'SPIDER_MIDDLEWARES': {
            # 'android_scrapy.loadmiddlewares.LoadSpiderMiddleware': 543,
        },
    }


    def start_requests(self):
        httpid = redis_instance.get('__running_http_').decode()
        httpid_obj_id = ObjectId(httpid)
        print('httpid' + httpid)
        http = mongo_instance.https.find_one(
            filter={'_id': httpid_obj_id})
        task_obj_id = http['taskid']
        task = mongo_instance.tasks.find_one(
            filter={'_id': task_obj_id})

        cookie_str = http['actionhome']['REQUEST_HEADERS']['Cookie'].replace(
            ' ', '')
        cookie_arr = cookie_str.split(';')
        cookies = {item.split('=')[0]: item.split('=')[1]
                   for item in cookie_arr}
        # cookies = {}
        # cookies = {i.key: i.value for i in cookie.values()}
        print('- cookies')
        print(cookies)
        print(task)
        FakeLoadParams.cookies['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = cookies['wap_sid2']
        FakeLoadParams.cookies['wxuin'] = cookies['wxuin']
        # FakeLoadParams.cookies['version'] = cookies['version']

        FakeLoadParams.params['__biz'] = http['biz']
        FakeLoadParams.params['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.params['appmsg_token'] = http['appmsg_token']

        print('- FakeLoadParams')
        print(FakeLoadParams)

        url = NORMAL_URLS.load
        arr = []
        for key, val in FakeLoadParams.params.items():
            print(key + '=' + val)
            arr.append(key + '=' + val)
        queryString = '?' + '&'.join(arr)
        print('- start_requests')
        # print(queryString)
        # print(headers)
        # print(cookies)

        return [scrapy.Request(url=url+queryString, headers=FakeLoadParams.headers, cookies=FakeLoadParams.cookies, callback=self.next_request, method='GET')]

    def next_request(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - in next_request: {} '.format(t))
        print(response.body.decode())

