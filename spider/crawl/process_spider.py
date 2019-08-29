import logging
import re
import urllib3
import json
import requests
import time
import datetime
from items.home_request import FakeHomeParams
from items.list_request import FakeLoadParams
from tools import replace_at_index
from tools.load_list_parse import list_into_dbdata, list_parse
from db.operate import LoadsOperate
from db.operate import TaskOperate

class NORMAL_URLS:
    home = "https://mp.weixin.qq.com/mp/profile_ext"
    load = "https://mp.weixin.qq.com/mp/profile_ext"
    article = "https://mp.weixin.qq.com/s"

class listSpider():
    """
    mode
    new_articles. [最新的, 到上次爬取的地方]  offset=0  title=''
    count_articles. [最新的, 到指定数量停止] offset=0 count%10次
    all_articles. [最新的, 到所有] offset=0 注意覆盖而已
    """
    # count 是10的倍数
    def __init__(self, rq, mode, count, crawl_min):
        self.rq = rq
        self.biz = rq['biz']
        # TODO
        self.title = ''
        self.end_article = {}
        if rq['start_article']:
            self.title = rq['start_article']['title']
        if rq['end_article']:
            self.end_article = rq['end_article']

        self.offset = 0

        self.mode = mode
        self.count = count
        self.crawl_min = crawl_min

    def prepare(self):
        print(' --- listSpider prepare ---')

        content = self.send_home_request()
        if not content:
            return
        pat = re.compile(r'window.appmsg_token = "(.*?)"')
        appmsg_token = pat.findall(content, pos=0)[0]
        self.build_load_request(appmsg_token)

    def run(self):
        switches = {
            'new_articles': self.run_crawl_new,
            'count_articles': self.run_crawl_count,
            'all_articles': self.run_crawl_all,
        }
        method = switches.get(self.mode)
        if method:
            method()



    def run_crawl_new(self):
        print(' --- run_crawl_new --- ')

        crawled_times = 0
        crawled_len = 0
        ss = ''
        recently_processed = 0
        l_in_db = {}
        start_articles = []
        stop_idx = None
        load_operate = LoadsOperate('load_operate')
        crawl_operate = TaskOperate('crawl_operate')
        while True :
            cur_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
            print('当前时间: ' + cur_time)
            # try:
            list_db_data = self.send_load_request()
            # print(list_db_data)
            recently_processed += 10
            crawled_len += len(list_db_data)
            crawled_times += 1

            if crawled_times == 1:
                for item in list_db_data:
                    if item['is_multi_app_msg_item_list'] == 'NO':
                        # print(item)
                        ss = item
                        break
                    else:
                        continue
                # TODO 万一不再这一次的爬取里面怎么办。。也就是crawled_times!=1
                # print(ss)

            start_articles = list_db_data

            if self.title != '':
                for idx, article in enumerate(start_articles):
                    if self.title == article['title']:
                        stop_idx = idx
                        print('找到了:  stop_idx {}'.format(stop_idx))
                        break
                else:
                    continue
                break
            else:
                if crawled_times == self.crawl_min / 10:
                    break

        # 数据入库
        try:
            if stop_idx != 0 :
                load_operate.save_list_to_db(start_articles[0::stop_idx])
        except Exception as db_err:
            print(db_err)
            raise Exception('save_list_to_db 数据库插入出错了')

            # except Exception as err:
            #     print('失败处理第 {} 个load请求，当前 offset= {} 一共爬取了{}个article'.format(
            #         crawled_times, self.offset, crawled_len))
            #     if str(err).find('无数据') > 0:
            #         break

        l_in_db['start_article'] = ss
        l_in_db['end_article'] = self.end_article
        l_in_db['recently_processed'] = recently_processed
        crawl_operate.update_crawldata_in_mongo(self.biz, l_in_db)


    def run_crawl_count(self):
        print(' --- run_crawl_count --- ')
        # return
        crawled_times = 0
        crawled_len = 0
        ss = ''
        ee = ''
        recently_processed = 0
        l_in_db = {}
        load_operate = LoadsOperate('load_operate')
        crawl_operate = TaskOperate('crawl_operate')
        while crawled_times < self.count / 10:
            cur_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
            print('当前时间: ' + cur_time)
            # try:
            list_db_data = self.send_load_request()
            # print(list_db_data)
            recently_processed += 10
            crawled_len += len(list_db_data)
            crawled_times += 1

            if crawled_times == 1:
                for item in list_db_data:
                    if item['is_multi_app_msg_item_list'] == 'NO':
                        # print(item)
                        ss = item
                        break
                    else:
                        continue
                # TODO 万一不再这一次的爬取里面怎么办。。也就是crawled_times!=1
                # print(ss)

            if crawled_times == self.count / 10:
                for item in reversed(list_db_data):
                    if item['is_multi_app_msg_item_list'] == 'NO':
                        ee = item
                        break
                    else:
                        continue
                # print(ee)

        # 数据入库
        try:
            load_operate.save_list_to_db(list_db_data)
        except Exception as db_err:
            print(db_err)
            raise Exception('save_list_to_db 数据库插入出错了')

            # except Exception as err:
            #     print('失败处理第 {} 个load请求，当前 offset= {} 一共爬取了{}个article'.format(
            #         crawled_times, self.offset, crawled_len))
            #     if str(err).find('无数据') > 0:
            #         break
        l_in_db['start_article'] = ss
        l_in_db['end_article'] = ee
        l_in_db['recently_processed'] = recently_processed
        crawl_operate.update_crawldata_in_mongo(self.biz, l_in_db)



    def run_crawl_all(self):
        pass

    def send_load_request(self):
        time.sleep(3)

        # 循环机制改变一下 需要捕捉到所有的真实错误
        # ANCHOR 测试结果 一天最多请求 1000次
        list_parse_res = {}
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 3, ('offset', self.offset))
        urllib3.disable_warnings()
        response = requests.get(
            NORMAL_URLS.load,
            headers=FakeLoadParams.headers,
            params=FakeLoadParams.params,
            cookies=FakeLoadParams.cookies,
            verify=False
        )

        if response.content.decode().find('操作频繁') > 0:
            print('操作频繁 限制24小时 请更换微信')
            return
        else:
            # 转一步，变成 { list : []} 结构
            list_parse_res = list_parse(eval(response.text))

        self.offset += len(list_parse_res['list'])
        print(' --- list_parse_res ---')
        # print(list_parse_res['list'])

        # 转两步，变成 [] 结构 并且取出里面还有可能有的 multiply list
        list_db_data = list_into_dbdata(list_parse_res)
        if not list_db_data:
            raise Exception('list_into_dbdata 后面无数据了')

        return list_db_data


    def build_load_request(self, appmsg_token):
        # print(appmsg_token)
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 1, ('__biz', FakeHomeParams.params[1][1]))

        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 11, ('appmsg_token', appmsg_token))

        # print(FakeLoadParams.headers)
        # print(FakeLoadParams.cookies)
        print(FakeLoadParams.params)


    def send_home_request(self):
        # response网络请求是同步
        urllib3.disable_warnings()
        response = requests.get(
            NORMAL_URLS.home,
            headers=FakeHomeParams.headers,
            params=FakeHomeParams.params,
            cookies=FakeHomeParams.cookies,
            verify=False
        )
        if response.content.decode().find('失效的验证页面') > 0:
            print('失效的验证页面')
            return

        if response.content.decode().find('操作频繁') > 0:
            print('操作频繁 限制24小时 请更换微信')
            return

        # print(response.content.decode())
        # login_cookies = requests.utils.dict_from_cookiejar(
        #     response.cookies)
        # print(login_cookies)
        # print('第二次的wap_sid2=' + login_cookies['wap_sid2'])
        # print('pass_ticket=' + login_cookies['pass_ticket'])
        # try:
        #     if login_cookies['pass_ticket']:
        #         FakeLoadParams.cookies['pass_ticket'] = login_cookies['pass_ticket']
        #         FakeLoadParams.params = replace_at_index(
        #             FakeLoadParams.params, 9, ('pass_ticket', login_cookies['pass_ticket']))

        #     if login_cookies['wap_sid2']:
        #         FakeLoadParams.cookies['wap_sid2'] = login_cookies['wap_sid2']

        # except Exception as err:
        #     print(err)
        #     print('无 pass_ticket 和 wap_sid2')

        return response.content.decode()




