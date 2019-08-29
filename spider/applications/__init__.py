import logging
import time
from crawl.get_redis_data import drop_data_from_redis, tidy_data
from crawl.process_spider import listSpider
# from phone.process_operate import phoneOperator
from phone.operate import Operate as phoneOperator
from db.operate import BizsOperate
from configs.crawler import CRAWL_MODE, CRAWL_COUNT, CRAWL_MIN




def proxy_listener(rqlist):
    pass


def data_crawler(rqlist):
    while True:
        print('loop redis-server中的数据...')
        time.sleep(10)
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


def phone_operator():
    bizname_operator = BizsOperate('bizname_operator')
    biznames = bizname_operator.find_all_biznames()

    for bizobj in biznames:
        # print(bizobj)
        phone_operate = phoneOperator(bizobj['fakename'], bizobj['chname'])
        phone_operate.home_click()
        phone_operate.search_text()
        phone_operate.tab_click()
        phone_operate.enter_into_gzh()

        break
        print('休息十秒')
        time.sleep(10)


    # client.home_click()
    # client.search_text()
    # client.tab_click()
    # client.enter_into_gzh()
