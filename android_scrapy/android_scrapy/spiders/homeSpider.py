import scrapy
from ..items import HomeItem

class HomeSpider(scrapy.Spider):
    name = 'HomeSpider'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = []

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
            # 'qq_news.middlewares.ProxyMiddleware': 543,
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
