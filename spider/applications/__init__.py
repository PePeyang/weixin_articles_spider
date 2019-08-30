import logging
import time
import random
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

        data = drop_data_from_redis()
        tidy_data(rqlist, data)

        # raise Exception('Hello')
        while not rqlist.isEmpty():
            single_redis = rqlist.popItem()
            lspider = listSpider(single_redis, CRAWL_MODE,
                                 CRAWL_COUNT, CRAWL_MIN)
            lspider.prepare()
            lspider.run()

        time.sleep(20)
    # TODO 可能会有错误的公众号数据
    # TODO 可能有的公众号不给key
    # TODO SSL ERROR


def phone_operator():
    bizname_operator = BizsOperate('bizname_operator')
    biznames = bizname_operator.find_all_biznames()

    for bizobj in biznames[0::]:
        # print(bizobj)
        phone_operate = phoneOperator(bizobj['fakename'], bizobj['fakename'])

        print(' --- home_click --- ')
        phone_operate.home_click()
        print(' --- search_text --- ')
        phone_operate.search_text()
        print(' --- click_souyisou --- ')
        phone_operate.click_souyisou()
        print(' --- enter_into_gzh --- ')
        phone_operate.enter_into_gzh()
        print(' --- enter_into_article --- ')
        phone_operate.enter_into_article()


        phone_operate.click_back_button()
        print(' --- click_back_button --- ')
        phone_operate.click_back_button()
        print(' --- click_back_button --- ')
        phone_operate.click_back_button()
        print(' --- click_back_button --- ')
        phone_operate.click_back_button()
        print(' --- click_back_button --- ')
        phone_operate.click_back_button()


        t = random.randint(3,4)
        print('休息{}秒'.format(t))
        time.sleep(t)
