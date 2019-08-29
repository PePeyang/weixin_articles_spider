import logging
import time
from crawl.get_redis_data import drop_data_from_redis, tidy_data
from crawl.process_spider import listSpider
from phone.operate import Operate
from configs.crawler import CRAWL_MODE, CRAWL_COUNT, CRAWL_MIN
# client = Operate('苏州青舞舞蹈艺术')
# operate_phone(client)


def proxy_listener(rqlist):
    # client = Operate('苏州青舞舞蹈艺术')
    pass


def data_crawler(rqlist):
    while True:
        print('loop redis-server中的数据...')
        time.sleep(6)
        data = drop_data_from_redis()
        tidy_data(rqlist, data)

        while not rqlist.isEmpty():
            single_redis = rqlist.popItem()
            lspider = listSpider(single_redis, CRAWL_MODE,
                                 CRAWL_COUNT, CRAWL_MIN)
            lspider.prepare()
            lspider.run()

    # TODO 可能会有错误的公众号数据
    # TODO 可能有的公众号不给key
    # TODO SSL ERROR


def phone_operator(client):
    pass
    # client.home_click()
    # client.search_text()
    # client.tab_click()
    # client.enter_into_gzh()
