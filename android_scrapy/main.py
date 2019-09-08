import scrapy
from android_scrapy.spiders.loadSpider import LoadSpider
from android_scrapy.spiders.articleSpider import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from instance import mongo_instance, redis_instance
import time
import sys, os

"""
ANCHOR
这里很丑陋，实在是太菜了，没法解决一些问题
1. 首先scrapy应当在项目外部启动，。。不会 我把这个文件搬出去以后 运行loadSpider 会卡在一个地方不继续了。
2. 这里的instance应当使用全局的instance。。。不会
3. 其实目前这里重启的是loadspider 但是应该重启的是整个process 不知道能不能做到。。。
4. 其实这里最好是 adb在操作以后 调用这个loadspider一次，再去调用articlespider一次。。。不会
这些问题没有解决，其实需要一次性调整一下项目结构就可以解决，但是我怎么调都一堆问题，还请大家帮帮忙 提提意见
"""

def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)



process = CrawlerProcess(get_project_settings())

def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print(
        '稍等。6秒后会自动重启...'))
    deferred.addCallback(sleep, seconds=6)
    deferred.addCallback(_crawl, spider)
    return deferred

suber = redis_instance.pubsub()
suber.subscribe('there_is_a_http')

try:
    while True:
        res = suber.parse_response()
        httpid = redis_instance.get('__running_http_')
        if httpid:
            # redis_instance.delete('__running_http_')
            print('检测到了新的的http')
            _crawl(None, LoadSpider)
            process.start()
        else:
            print('没有成功捕获到新的http')
            # _crawl(None, ArticleSpider)
        time.sleep(2)
except KeyboardInterrupt:
    print("优雅的手动停止...")
    sys.exit(1)
