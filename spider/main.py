# 构造home请求获取 appmsg_token
# 构造分页请求
#
from tools.load_list_parse import list_into_dbdata, list_parse
from phone.operate import Operate
from instance import redis_instance, db_instance, db_loadlist
import json
import re



def operate_phone(client):
    client.home_click()
    # client.search_text()
    # client.tab_click()
    # client.enter_into_gzh()


if __name__ == '__main__':
    print('__main__')

    from crawl.get_redis_data import get_data_from_redis, tidy_data
    from crawl.process_spider import listSpider

    data = get_data_from_redis()
    rqlist = tidy_data(data)
    print(' --- rqlist --- ')
    print(rqlist)

    # TODO 可能会有错误的公众号数据
    # TODO 可能有的公众号不给key

    while not rqlist.isEmpty():
        rq = rqlist.popItem()
        # print(rq)
        lspider = listSpider(rq, 'count_articles', 20)
        lspider.prepare()
        lspider.run()


    # client = Operate('苏州青舞舞蹈艺术')
    # operate_phone(client)









