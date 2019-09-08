# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http.request import Request
from scrapy import signals
import datetime
import scrapy
from .spider_config import FakeLoadParams
from instance import mongo_instance, redis_instance
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
import re
import os
import requests


class ArticleSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        print(' - 2、 process_spider_input')
        # Should return None or raise an exception.
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        # print(' - 3、 parse')
        body_html = response.body.decode()
        # bf_html = BeautifulSoup(body_html, 'html.parser')
        # print(body_html)
        pat_get_meta_url = re.compile(r'data-src="(https://.*?)"')
        pat_get_meta_type = re.compile(r'wx_fmt=(.*)')


        chname = spider.chname
        title = spider.title
        # print(title)

        sdir1 = os.path.join(os.path.abspath(''), "output", chname)
        sdir2 = os.path.join(sdir1, title)

        mats = pat_get_meta_url.findall(body_html, pos=0)
        idx = 0

        if not os.path.exists(sdir1):
            os.mkdir(sdir1)
            os.mkdir(sdir2)
        elif not os.path.exists(sdir2):
            os.mkdir(sdir2)

        with open(os.path.join(sdir2, 'index.html').replace("\\", "/"),
                  'wb') as f:
            f.write(response.body)

        for m in mats:
            idx += 1
            pps = pat_get_meta_type.findall(m)
            if pps:
                postfix = pps[0]
            else:
                postfix = 'jpg'
            # 这里是给图片命名的地方

            # print(os.path.join(sdir2, "{}.{}".format(idx, postfix)))
            self.download(
                m,
                os.path.join(sdir2,
                             "{}.{}".format(idx, postfix)).replace("\\", "/"))
        return None

    def download(self, url, sname):
        for i in range(0, 3):
            result = requests.get(
                url,
                headers={
                    'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
                },
                stream=True)
            if result.status_code == 200:
                with open(sname, 'wb') as f:
                    for chunk in result.iter_content(1024):
                        f.write(chunk)
                return True
            else:
                continue
        print("Error download")
        return False

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        print(' - 4、 process_spider_output')

        # Must return an iterable of Request, dict or Item objects.

        # print(response)
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        print(exception)
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).

        print(' - 1、 process_start_requests')
        for load in spider.loads:
            print(load)
            spider.title = load['title']
            spider._id = load['_id']
            spider.url = load['content_url']
            spider.chname = load['chname']
            t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
            # mongo_instance.loads.delete_one({"_id": spider._id})
            yield scrapy.Request(url=spider.url,
                                 headers=FakeLoadParams.headers,
                                 method='GET')

    def spider_opened(self, spider):
        spider.logger.info('ArticleSpiderMiddleware: Spider opened: %s' %
                           spider.name)

        loads = mongo_instance.loads.find().limit(1)
        spider.logger.info(loads)
        spider.loads = loads


class LoadDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        print(exception)
        pass

    def spider_opened(self, spider):
        spider.logger.info('LoadDownloaderMiddleware: Spider opened: %s' %
                           spider.name)
