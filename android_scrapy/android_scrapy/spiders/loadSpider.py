import datetime
import scrapy
import re
from ..items import HomeItem
from spider_config import FakeLoadParams, NORMAL_URLS
from bson.objectid import ObjectId
from instance.main_instance import mongo_instance, redis_instance
from http.cookies import SimpleCookie
from w3lib.url import add_or_replace_parameter
from w3lib.url import url_query_parameter
from load_list_parse import list_parse, list_into_dbdata

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
        "DOWNLOAD_DELAY": 3,
        "COOKIES_ENABLED": True
    }


    def start_requests(self):
        http = self.http
        task = self.task

        cookie_str = http['actionhome']['REQUEST_HEADERS']['Cookie'].replace(
            ' ', '')
        cookie_arr = cookie_str.split(';')
        # NOTE 我曹！
        cookies = {item.split('=', 1)[0]: item.split('=', 1)[1]
                   for item in cookie_arr}
        print('- cookies')
        print(cookies)

        FakeLoadParams.cookies['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = cookies['wap_sid2']
        FakeLoadParams.cookies['wxuin'] = cookies['wxuin']
        FakeLoadParams.cookies['version'] = cookies['version']

        FakeLoadParams.params['__biz'] = http['biz']
        FakeLoadParams.params['pass_ticket'] = http['pass_ticket']
        FakeLoadParams.params['appmsg_token'] = http['appmsg_token']

        url = NORMAL_URLS.load
        arr = []
        for key, val in FakeLoadParams.params.items():
            # print(val)
            arr.append(key + '=' + val)
        queryString = '?' + '&'.join(arr)
        print(queryString)
        print('- FakeLoadParams cookies')
        print(FakeLoadParams.cookies)
        self.crawled_times = 1
        if self.task['task_status'] == 'running':
            yield scrapy.Request(url=url+queryString, headers=FakeLoadParams.headers, cookies=FakeLoadParams.cookies, method='GET')
        else:
            return

    def parse(self, response):
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' - in next_request: {} '.format(t))
        print(response.url)
        print(response.body.decode())

        """
        可以继续爬取的条件
        new: ret = 0 and can_msg_continue = 1 and 转换后的list中没有出现start_article中的list
        按量：ret = 0 and can_msg_continue = 1 and count <= crawl_count
        all: ret = 0 and can_msg_continue = 1
        """

        switches = {
            'new': self.run_crawl_new,
            'count': self.run_crawl_count,
            'all': self.run_crawl_all,
        }
        method = switches.get(self.task['task_mode'])
        return method(response)

    def run_crawl_new(self, response):
        next_offset = int(url_query_parameter(response.url, 'offset')) + 10
        print(' --- run_crawl_new --- ')
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        list_parse_res = list_parse(eval(response.body.decode()))
        list_db_data = list_into_dbdata(
            list_parse_res, self.task['task_biz_enname'], self.task['task_biz_chname'], self.task['_id'])

        # 到头了或者出错了
        if not list_db_data:
            self.task['task_status'] = 'end_success'
            return

        load_obj_id = self.task['task_start_loadid']
        print(load_obj_id)
        stop_idx = None

        # 不是公众号第一次的话，就要找到一个位置停下
        if load_obj_id == None:
            pass
        else:
            load = mongo_instance.loads.find_one(
                filter={"_id": load_obj_id})
            title = load['title']
            print(title)
            for idx, item in enumerate(list_db_data):
                if item['is_multi_app_msg_item_list'] == 'NO' and title == item['title']:
                    stop_idx = idx
                    print('找到了:  stop_idx {}'.format(idx))
                    self.task['task_status'] = 'end_success'
                    break
                else:
                    pass


        if self.crawled_times == self.task['task_crawl_min'] / 10:
            self.task['task_status'] = 'end_success'
            print('要出去了')
        else:
            pass

        res = None
        if stop_idx == None:
            res = mongo_instance.loads.insert_many(list_db_data)
        elif stop_idx == 0:
            pass
        elif stop_idx != 0:
            res = mongo_instance.loads.insert_many(list_db_data[0::stop_idx])

        if self.crawled_times == 1 and res != None:
            print(' 插入的第一个id是: %s' % res.inserted_ids[0])
            self.task['task_start_loadid'] = res.inserted_ids[0]
        else:
            pass

        self.task['task_updatetime'] = t
        self.task['task_endtime'] = t
        mongo_instance.tasks.find_one_and_update(
            filter={'_id': self.task['_id']}, update={
                '$set': self.task
            })


        if self.task['task_status'] != 'running':
            return
        else:
            self.crawled_times += 1
            yield scrapy.Request(url=add_or_replace_parameter(response.url, 'offset', next_offset), headers=FakeLoadParams.headers, cookies=FakeLoadParams.cookies, method='GET')

    def run_crawl_count(self, response):
        next_offset = int(url_query_parameter(response.url, 'offset')) + 10
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' --- run_crawl_count --- ')
        list_parse_res = list_parse(eval(response.body.decode()))
        list_db_data = list_into_dbdata(
            list_parse_res, self.task['task_biz_enname'], self.task['task_biz_chname'], self.task['_id'])

        # 到头了或者出错了
        if not list_db_data:
            self.task['task_status'] = 'end_success'
            return

        if self.crawled_times == self.task['task_crawl_count'] / 10:
            self.task['task_status'] = 'end_success'
            print('要出去了')
        else:
            res = mongo_instance.loads.insert_many(list_db_data)
            if self.crawled_times == 1:
                print(' 插入的第一个id是: %s' % res.inserted_ids[0])
                self.task['task_start_loadid'] = res.inserted_ids[0]

        self.task['task_updatetime'] = t
        self.task['task_endtime'] = t
        mongo_instance.tasks.find_one_and_update(
            filter={'_id': self.task['_id']}, update={
                '$set': self.task
            })


        if self.task['task_status'] != 'running':
            return
        else:
            self.crawled_times += 1
            yield scrapy.Request(url=add_or_replace_parameter(response.url, 'offset', next_offset), headers=FakeLoadParams.headers, cookies=FakeLoadParams.cookies, method='GET')

    def run_crawl_all(self, response):
        next_offset = int(url_query_parameter(response.url, 'offset')) + 10
        t = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        print(' --- run_crawl_all --- ')
        list_parse_res = list_parse(eval(response.body.decode()))
        list_db_data = list_into_dbdata(
            list_parse_res, self.task['task_biz_enname'], self.task['task_biz_chname'], self.task['_id'])

        # 到头了或者出错了
        if not list_db_data:
            self.task['task_status'] = 'end_success'
            print('要出去了')
            return
        else:
            res = mongo_instance.loads.insert_many(list_db_data)
            if self.crawled_times == 1:
                print(' 插入的第一个id是: %s' % res.inserted_ids[0])
                self.task['task_start_loadid'] = res.inserted_ids[0]

        self.task['task_updatetime'] = t
        self.task['task_endtime'] = t
        mongo_instance.tasks.find_one_and_update(
            filter={'_id': self.task['_id']}, update={
                '$set': self.task
            })

        if self.task['task_status'] != 'running':
            return
        else:
            yield scrapy.Request(url=add_or_replace_parameter(response.url, 'offset', next_offset), headers=FakeLoadParams.headers, method='GET')
