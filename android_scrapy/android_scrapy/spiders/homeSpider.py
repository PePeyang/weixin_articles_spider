import datetime
import scrapy
import re
from ..items import HomeItem
from config import FakeLoadParams
from config import FakeHomeParams
from config import NORMAL_URLS
from scrapy.http import TextResponse

class HomeSpider(scrapy.Spider):
    name = 'HomeSpider'
    # allowed_domains = ['mp.weixin.qq.com']
    # start_urls = ['https://www.baidu.com']
    t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(' - {} HomeSpider开始爬取了..'.format(t))
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
            # 'zhihu_topic.pipelines.ZhihuTopicPipeline': 301,
            # 'zhihu_topic.pipelines.RedisStartUrlsPipeline': 304,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'android_scrapy.homemiddlewares.HomeDownloaderMiddleware': 543,
        },
        'SPIDER_MIDDLEWARES': {
            'android_scrapy.homemiddlewares.HomeSpiderMiddleware': 543,
        },

        'FEED_EXPORT_ENCODING': 'utf-8',
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.3.2000",

        'DEFAULT_REQUEST_HEADERS': {
            "HOST": "mp.weixin.qq.com",
            "Referer": "https://mp.weixin.qq.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/55.0.2883.75 Safari/537.36 Maxthon/5.1.3.2000"
        }
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

        return [scrapy.Request(url=url+queryString, headers=headers, cookies=cookies, callback=self.next_request, method='GET')]

    def next_request(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - in next_request: {} '.format(t))
        # print(response.body.decode())
        if response.body.decode().find('失效的验证页面') > 0:
            print('失效的验证页面')
            return

        if response.body.decode().find('操作频繁') > 0:
            print('操作频繁 限制24小时 请更换微信')
            return

        pat = re.compile(r'window.appmsg_token = "(.*?)"')
        appmsg_token = pat.findall(response.body.decode(), pos=0)[0]
        self.build_load_request(appmsg_token)

    def build_load_request(self, appmsg_token):
        # print(appmsg_token)
        FakeLoadParams.params['__biz'] = FakeHomeParams.params['__biz']
        FakeLoadParams.params['appmsg_token'] = FakeHomeParams.params['appmsg_token']
        print('- build_load_request 成功替换了__biz 和 appmsg_token：')
        print(FakeLoadParams.params)
