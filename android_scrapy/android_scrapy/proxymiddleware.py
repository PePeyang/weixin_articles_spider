import json
import requests
import logging
import os
import re
import time


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        rp = os.path.abspath('.')
        self.ippath = os.path.join(rp, 'ip.txt').replace('\\', '/')

    def get_random_proxy(self):
        oldproxy = None
        with open(self.ippath, 'r+', encoding='utf-8-sig') as f:  # 打开文件
            oldproxy = f.readline()
        self.logger.debug('get_random_proxy')
        self.logger.debug(oldproxy)
        # return None
        try:
            if self.check_proxy(oldproxy):
                self.logger.debug('使用了旧的代理')
                return oldproxy
            else:
                self.logger.debug('旧的代理不行1')
                return self.get_a_proxy()
        except:
            self.logger.debug('旧的代理不行2')
            return self.get_a_proxy()

    def get_a_proxy(self):
        # return None
        response = requests.get(self.proxy_url)
        if response.status_code == 200:
            try:
                proxy = response.text.strip()
                self.logger.debug('拉取到的东西 %s' % proxy)
            except:
                self.logger.debug('拉到的代理错误')
                return self.get_a_proxy()

            try:
                proxy = self.check_proxy(proxy)
            except:
                self.logger.debug('这次白白获取了')
                return self.get_a_proxy()

            if proxy:
                with open(self.ippath, 'w', encoding='utf-8-sig') as f:  # 打开文件
                    f.write(proxy)
                return proxy
            self.logger.debug('写入文件失败')
            return proxy

        else:
            time.sleep(1)
            self.logger.debug('code不为两百')
            return self.get_a_proxy()

    def check_proxy(self, proxy):
        if not proxy:
            return

        ip = {"https": "https://" + proxy}
        r = requests.get("https://www.baidu.com",
                         proxies=ip,
                         timeout=4,
                         allow_redirects=True,
                         verify=False)
        if r.status_code == 200:
            return proxy

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("again response ip:")
            request.meta['proxy'] = 'http://{proxy}'.format(
                proxy=self.get_random_proxy())
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'))
