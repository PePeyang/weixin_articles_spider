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
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_parameter

class LoadSpider(scrapy.Spider):
    name = 'LoadSpider'
    allowed_domains = ['mp.weixin.qq.com']
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
            'android_scrapy.loadmiddlewares.LoadSpiderMiddleware': 543,
        },
        # 设置请求间隔
        "DOWNLOAD_DELAY": 10,
        "COOKIES_ENABLED": True
    }


    def start_requests(self):
        http = self.http
        task = self.task

        cookie_str = http['actionhome']['REQUEST_HEADERS']['Cookie'].replace(
            ' ', '')
        cookie_arr = cookie_str.split(';')
        cookies = {item.split('=')[0]: item.split('=')[1]
                   for item in cookie_arr}
        print('- cookies')
        print(cookies)

        FakeLoadParams.cookies['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = cookies['wap_sid2']
        FakeLoadParams.cookies['wxuin'] = cookies['wxuin']
        # FakeLoadParams.cookies['version'] = cookies['version']

        FakeLoadParams.params['__biz'] = http['biz']
        FakeLoadParams.params['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.params['appmsg_token'] = http['appmsg_token']

        url = NORMAL_URLS.load
        arr = []
        for key, val in FakeLoadParams.params.items():
            print(val)
            arr.append(key + '=' + val)

        queryString = '?' + '&'.join(arr)

        print(queryString)
        yield scrapy.Request(url=url+queryString, headers=FakeLoadParams.headers, cookies=FakeLoadParams.cookies, method='GET')



    def parse(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - in next_request: {} '.format(t))
        print(response.url)
        print(response.body.decode()[0::100])

        next_offset = int(url_query_parameter(response.url, 'offset')) + 10
        yield scrapy.Request(url=add_or_replace_parameter(response.url, 'offset', next_offset), headers=FakeLoadParams.headers, method='GET')


