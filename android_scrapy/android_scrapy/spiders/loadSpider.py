import datetime
import scrapy
import re
from ..items import HomeItem
from config import FakeLoadParams
from config import FakeHomeParams
from config import NORMAL_URLS
from scrapy.http import TextResponse

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
            'android_scrapy.loadmiddlewares.LoadSpiderMiddleware': 543,
        },
    }


    def start_requests(self):
        url = NORMAL_URLS.home
        headers = FakeHomeParams.headers
        cookies = FakeHomeParams.cookies
        params = FakeHomeParams.params
        arr = []
        for key,val in params.items():
            print(key + '=' + val)
            arr.append(key + '=' + val)
        queryString = '?' + '&'.join(arr)
        print('- start_requests')
        print(queryString)
        print(headers)
        print(cookies)
        return [scrapy.Request(url=url+queryString, headers=headers, cookies=cookies, callback=self.next_request, method='GET')]

    def next_request(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - in next_request: {} '.format(t))


