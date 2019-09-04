import os
import sys
from threading import Thread
import datetime
from process_scrapy import start_scrapy_loads
from scrapy import cmdline

class SCRAPY_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            start_scrapy_loads()
        except BaseException as be:
            print(be)
            # self.run()

    def join(self):
        Thread.join(self)


if __name__ == '__main__':
    # signal.signal(signal.SIGINT, quit)
    # signal.signal(signal.SIGTERM, quit)

    # 启动 SCRAPY_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} SCRAPY_THREAD 启动中...'.format(bftime))
    t = SCRAPY_THREAD()
    t.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} SCRAPY_THREAD 已启动'.format(aftime))
    t.join()
    fftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} SCRAPY_THREAD 已结束'.format(fftime))


# os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'myproject.settings')
# settings.overrides['LOG_ENABLED'] = False  # avoid log noise


# def item_passed(item):
#     print "Just scraped item:", item


# dispatcher.connect(item_passed, signal=signals.item_passed)

# crawler = CrawlerThread()
# print "Starting crawler thread..."
# crawler.start()

# crawler.crawl('LoadSpider')  # blocking call
# print "Crawling anotherdomain.com..."
# crawler.crawl('anotherdomain.com')  # blocking call
# print "Stopping crawler thread..."
# crawler.stop()
