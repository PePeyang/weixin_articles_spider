import re
import requests
import datetime
from items.home_request import FakeHomeParams
from items.list_request import FakeLoadParams
from tools import replace_at_index
from tools.load_list_parse import list_into_dbdata, list_parse
from db.operate import LoadsOperate

class NORMAL_URLS:
    home = "https://mp.weixin.qq.com/mp/profile_ext"
    load = "https://mp.weixin.qq.com/mp/profile_ext"
    article = "https://mp.weixin.qq.com/s"

class listSpider():
    def __init__(self, rq):
        self.rq = rq
        self.offset = rq['offset']

    def start(self):
        print(' --- listSpider start ---')

        content = self.send_home_request()
        if not content:
            return

        pat = re.compile(r'window.appmsg_token = "(.*?)"')
        appmsg_token = pat.findall(content, pos=0)[0]

        self.build_load_request(appmsg_token)
        # self.loop_request_load()

    def build_load_request(self, appmsg_token):
        # print(appmsg_token)
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 1, ('__biz', FakeHomeParams.params[1][1]))

        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 11, ('appmsg_token', appmsg_token))

        # print(FakeLoadParams.headers)
        # print(FakeLoadParams.cookies)
        # print(FakeLoadParams.params)


    def send_home_request(self):
        # response网络请求是同步
        response = requests.get(NORMAL_URLS.home,
                                headers=FakeHomeParams.headers, params=FakeHomeParams.params, cookies=FakeHomeParams.cookies)
        if response.content.decode().find('失效的验证页面') > 0:
            print('失效的验证页面')
            return

        if response.content.decode().find('操作频繁') > 0:
            print('操作频繁 限制24小时 请更换微信')
            return

        # print(response.content.decode())
        login_cookies = requests.utils.dict_from_cookiejar(
            response.cookies)
        print(login_cookies)
        # print('第二次的wap_sid2=' + login_cookies['wap_sid2'])
        # print('pass_ticket=' + login_cookies['pass_ticket'])
        FakeLoadParams.cookies['pass_ticket'] = login_cookies['pass_ticket']
        FakeLoadParams.cookies['wap_sid2'] = login_cookies['wap_sid2']
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 9, ('pass_ticket', login_cookies['pass_ticket']))

        return response.content.decode()


    def send_load_request(self):
        # 每次请求十条
        FakeLoadParams.params = replace_at_index(
            FakeLoadParams.params, 3, ('offset', self.offset))


        response = requests.get(
            NORMAL_URLS.load,
            headers=FakeLoadParams.headers,
            params=FakeLoadParams.params,
            cookies=FakeLoadParams.cookies
        )

        if response.content.decode().find('操作频繁') > 0:
            print('操作频繁 限制24小时 请更换微信')
        else:
            return eval(response.text)


    def loop_request_load(self):
        import time
        print(datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
        load_operate = LoadsOperate('load_operate')
        idx=0
        items_len=0
        # 循环机制改变一下 需要捕捉到所有的真实错误
        # ANCHOR 测试结果 一天最多请求 1000次
        while True:
            try:

                list_parse_res = list_parse(eval(self.send_load_request()))

                # 转一步，变成 { list : []} 结构
                if type(list_parse_res['ret']) == type(0):
                    print(list_parse_res)
                    raise Exception('list_parse_res 数据parse失败了')
                self.offset += len(list_parse_res['list'])

                # 转两步，变成 [] 结构 并且取出里面还有可能有的 multiply list
                list_db_data = list_into_dbdata(list_parse_res)
                if not list_db_data:
                    raise Exception('list_into_dbdata 后面无数据了')

                # 数据入库
                try:
                    load_operate.save_list_to_db(list_db_data)
                    print('成功处理第 {} 个load请求，当前 offset= {} items_len= {}'.format(
                        idx, self.offset, items_len))
                except Exception as db_err:
                    print(db_err)
                    raise Exception('save_list_to_db 数据库插入出错了')
                items_len += len(list_db_data)


                time.sleep(3)

            except Exception as err:
                print('失败处理第 {} 个load请求，当前 offset= {} items_len= {}'.format(
                    idx, self.offset, items_len))
                print(err)
                if str(err).find('无数据') > 0:
                    break
        print(datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
