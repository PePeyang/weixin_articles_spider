# -*- coding:utf-8 -*-
import time
# import signal
import sys
from threading import Thread
import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater

from android.process_adb import adb_entry
from android.process_listen import listen_task_entry

# from android_scrapy.android_scrapy.spiders.loadSpider import LoadSpider
from instance.main_instance import mongo_instance, redis_instance


class ADB_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        adb_entry()

    def join(self):
        Thread.join(self)

class LITEN_TASK_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        listen_task_entry()

    def join(self):
        Thread.join(self)


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)

if __name__ == '__main__':

    # 启动 LITEN_TASK_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 启动中...'.format(bftime))
    t_listen = LITEN_TASK_THREAD()
    t_listen.daemon = True
    t_listen.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 已启动'.format(aftime))

    # 启动 ADB_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 启动中...'.format(bftime))
    t_adb = ADB_THREAD()
    t_adb.daemon = True
    t_adb.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 已启动'.format(aftime))

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print('t_listen正在停止中。。。')
        t_listen.join()
        print('t_adb正在停止中。。。')
        t_adb.join()
# process = CrawlerProcess(get_project_settings())

# def _crawl(result, spider):
#     deferred = process.crawl(spider)
#     deferred.addCallback(lambda results: print(
#         '稍等。1秒后会自动重启...'))
#     deferred.addCallback(sleep, seconds=1)
#     deferred.addCallback(_crawl, spider)
#     return deferred


# while True:
#     httpid = redis_instance.get('__running_http_')
#     if httpid:
#         print('检测到了新的的http')
#         _crawl(None, LoadSpider)
#         process.start()
#     else:
#         print('没有成功捕获到的http')
#     time.sleep(30)
