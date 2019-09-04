import json
import requests
import logging
import os
import re
import time
# with open(self.ippath, 'r+') as f:  # 打开文件
#     oldip = f.readline()

# with open(self.ippath, 'w') as f:  # 打开文件
#     f.write(ip)


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url
        rp = os.path.abspath('.')
        self.ippath = os.path.join(rp, 'ip.txt')

    def get_random_proxy(self):
        oldproxy = None
        with open(self.ippath, 'r+') as f:  # 打开文件
            oldproxy = f.readline()

        try:
            if self.check_proxy(oldproxy):
                self.logger.debug('使用了旧的代理')
                return oldproxy
        except:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text.strip()
                self.logger.debug('拉取到的代理 %s' % proxy)
                try:
                    proxy = self.check_proxy(proxy)
                except:
                    self.logger.debug('这次白白获取了')
                    return

                if proxy:
                    with open(self.ippath, 'w') as f:  # 打开文件
                        f.write(proxy)
                    return proxy

    def check_proxy(self, proxy):
        if not proxy:
            return

        ip = {"http": "http://" + proxy}
        r = requests.get("http://www.baidu.com", proxies=ip, timeout=4)
        if r.status_code == 200:
            return proxy

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        if proxy:
            self.logger.debug('======' + '使用代理 ' + str(proxy) + "======")
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=proxy)

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("again response ip:")
            request.meta['proxy'] = 'https://{proxy}'.format(
                proxy=self.get_random_proxy())
            return request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'))
