from scrapy import cmdline
from instance import redis_instance, mongo_instance
import time

def start_scrapy_home():
    cmdline.execute('scrapy crawl HomeSpider'.split())

def start_scrapy_loads():

    while True:
        httpid_b = redis_instance.get('__running_http_')

        if httpid_b:
            cmdline.execute('scrapy crawl LoadSpider'.split())
        else:
            print('没有成功捕获到的http')
        time.sleep(30)
