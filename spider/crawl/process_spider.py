import requests
from items.home_request import FakeHomeParams
from items.list_request import FakeLoadParams
from tools import replace_at_index

class NORMAL_URLS:
    home = "https://mp.weixin.qq.com/mp/profile_ext"
    getmsg = "https://mp.weixin.qq.com/mp/profile_ext"
    article = "https://mp.weixin.qq.com/s"

class listSpider():
    def __init__(self, rq):
        self.rq = rq

    def start(self):
        print(' --- listSpider start ---')
        self.send_home_request()

        pass

    # def build_load_request(appmsg_token):
    #     print(appmsg_token)

    #     FakeLoadParams.params = replace_at_index(
    #         FakeLoadParams.params, 1, ('__biz', FakeHomeParams.params[1][1]))

    #     FakeLoadParams.params = replace_at_index(
    #         FakeLoadParams.params, 11, ('appmsg_token', appmsg_token))

    #     print(FakeLoadParams.headers)
    #     print(FakeLoadParams.cookies)
    #     print(FakeLoadParams.params)

    def send_home_request(self):
        response = requests.get(NORMAL_URLS.home,
                                headers=FakeHomeParams.headers, params=FakeHomeParams.params, cookies=FakeHomeParams.cookies)
        if response.content.decode().find('失效的验证页面') > 0:
            print('失效的验证页面')
        else:
            login_cookies = requests.utils.dict_from_cookiejar(response.cookies)
            print('第二次的wap_sid2=' + login_cookies['wap_sid2'])
            print('pass_ticket=' + login_cookies['pass_ticket'])
            FakeLoadParams.cookies['pass_ticket'] = login_cookies['pass_ticket']
            FakeLoadParams.cookies['wap_sid2'] = login_cookies['wap_sid2']
            FakeLoadParams.params = replace_at_index(
                FakeLoadParams.params, 9, ('pass_ticket', login_cookies['pass_ticket']))
            return response.content.decode()

