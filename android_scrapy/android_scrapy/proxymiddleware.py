import json
import requests
import logging
import os
import re
import time

"""
购买的代理ip返回格式如下所示
{
    "code": "0",
    "msg": [
        {
            "port": "35277",
            "ip": "49.87.23.194"
        }
    ]
}
"""
class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        rp = os.path.abspath('.')
        self.ippath = os.path.join(rp, 'ip.txt').replace('\\', '/')

    def get_random_proxy(self, proto, proxy_url):
        oldproxy = None
        try:
            with open(self.ippath, 'r+', encoding='utf-8-sig') as f:  # 打开文件
                oldproxy = f.readline()
                print('取得的旧代理为' + oldproxy)
        except Exception as err:
            print('读取已有代理文件失败：')
            print(err)
            return self.get_random_proxy(proto, proxy_url)

        ip = oldproxy.split(':')[0]
        port = oldproxy.split(':')[1]

        if self.check_proxy(ip, port, proto):
            print('旧代理可以使用')
            return proto + '://' + oldproxy
        else:
            print('旧的代理不可使用，请求新代理...')
            proxy = self.get_a_proxy(proxy_url)
            print(proxy)
            while not proxy:
                print('重复获取可用的代理中')
                proxy = self.get_a_proxy(proxy_url)

            proxy_str = proxy['ip'] + ":" + proxy['port']

            try:
                with open(self.ippath, 'w', encoding='utf-8-sig') as f:  # 打开文件
                    f.write(proxy_str)
            except Exception as err:
                print('写入新的代理失败！')
                print(err)

            return self.get_random_proxy(proto, proxy_url)

    def get_a_proxy(self, proxy_url):
        try:
            response = requests.get(proxy_url)
        except Exception as err:
            print('请求失败！')
            print(err)
            return None

        if response.status_code != 200:
            print('获取代理响应失败')
            return None
        else:
            result = eval(response.text.strip())
            if result['code'] != "0":
                return None
            else:
                print(result['msg'])
                return result['msg'][0]

    def check_proxy(self, ip, port, proto):
        if proto != 'http' and proto != 'https':
            print('http协议设置错误！')
            return False
        proxy = {proto: "{proto}://{ip}:{port}".format(proto=proto,ip=ip, port=port)}

        try:
            r = requests.get("{}://icanhazip.com".format(proto), proxies=proxy, timeout=3)
            if r.status_code == 200 and r.text.strip() == ip:
                return True
            else:
                print(r.text.strip())
                print('检验代理时状态码不是200，可能是用来测试的网址失效了 icanhazip.com')
                return False
        except Exception as err:
            print('检验代理时抛出异常如下：')
            print(err)
            return False

    def process_request(self, request, spider):
        """
        FIXME 这里 request.meta['proxy'] = proxy 如果使用https代理会报错，不知道什么原因
        """
        proxy = self.get_random_proxy('http', self.proxy_url)
        if proxy:
            self.logger.debug('======' + '最终使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("使用代理请求真实地址未能成功")
            proxy = self.get_random_proxy('http', self.proxy_url)
            request.meta['proxy'] = proxy
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'))
