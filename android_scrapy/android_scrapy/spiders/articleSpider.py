import datetime
import scrapy
import re
from bson.objectid import ObjectId
from spider_config import FakeLoadParams
from instance import mongo_instance, redis_instance
from http.cookies import SimpleCookie
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_parameter
# from load_list_parse import list_parse, list_into_dbdata

class ArticleSpider(scrapy.Spider):
    name = 'ArticleSpider'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = []
    custom_settings = {
        # midlewares
        'ITEM_PIPELINES': {},
        'SPIDER_MIDDLEWARES': {
            'android_scrapy.articlemiddlewares.ArticleSpiderMiddleware': 543
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapy.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
            # 'android_scrapy.proxymiddleware.ProxyMiddleware': 543,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None
        },
        # 设置请求间隔
        "DOWNLOAD_DELAY": round(2, 5),
        "COOKIES_ENABLED": True,
    }


    def parse(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - 3、 parse')

        print(response.body.decode())


