# -*- coding: utf-8 -*-
# TODO 自定义类
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import re
import os
import json
import traceback
import random
import math
import codecs
import datetime
import lxml
import pymongo

class Session:
    token = ''
    cookies = []
    # TODO headers User-Agent 定期自动替换
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

class Urls:
    index = 'https://mp.weixin.qq.com'
    # editor = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token={token}'
    query_biz = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={token}&lang=zh_CN&f=json&ajax=1&random={random}&query={query}&begin={begin}&count={count}'
    query_arti = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&%E2%80%A65&action=list_ex&begin={begin}&count={count}&query={query}&fakeid={fakeid}&type=9'


class Spider:
    def __init__(self):
        print('Spider init...')
        self.connect_mongodb()


    def __del__(self):
        print('Spider delete...')
        self.close_mongodb()

    def main(self):
        print('mian')
        # /usr/bin/chromedriver
        chrome = input('请输入chromedriver路径 (注意要和自己的chrome版本匹配):').strip()
        if not chrome:
            if os.path.isfile('/usr/bin/chromedriver'):
                chrome = '/usr/bin/chromedriver'
            else:
                print('没有合适的chromedriver，程序无法进行！')
                return

        driver = webdriver.Chrome(executable_path=chrome)
        print('Succeed to load driver')
        self.do_weixin_login(driver)
        self.do_unfinish_work()
        return

    # 微信首页的登陆
    def do_weixin_login(self, driver):
        if not driver:
            print('Are you kidding me ？没有driver玩毛线')
            return
        base_dir = os.path.dirname(__file__)
        cookies_path = os.path.join(base_dir, 'caches/cookies.json')
        cookies = json.load(open(cookies_path, 'rb')
                            ) if os.path.isfile(cookies_path) else []
        driver.get(Urls.index)
        if not cookies:
            # TODO 自动输入账号密码 给出二维码然后自动登陆 只需要自己扫个码
            # ANCHOR cookie一般一天就到期
            input("请先手动登录, 完成后按回车继续:")
            cookies = driver.get_cookies()
            open(cookies_path, 'wb').write(json.dumps(cookies).encode('utf-8'))
        self.set_cookies(driver, cookies)
        # 这一步不能少
        driver.get(Urls.index)
        self.set_token(driver.current_url)
        return

    # 进行上次未完成的任务
    def do_unfinish_work(self):
        fakenames = self.db.fakenames
        fake_one = fakenames.find_one_and_delete(filter={})
        while fake_one:
            print(fake_one)
            self.pipe(fake_one['fakename'], fake_one['chname'])
            fake_one = fakenames.find_one_and_delete(filter={})

    def pipe(self, fakename, chname):
        # TODO 不止一页，以后要把所有查询到的都添加进数据库
        # 测试数据，这里找了13个公众号后就不行了，{"base_resp":{"ret":200013,"err_msg":"freq control"}}
        rep = requests.get(Urls.query_biz.format(random=random.random(), token=Session.token,
                                                 query=fakename, begin=0, count=5), cookies=Session.cookies, headers=Session.headers)
        print(rep.text)

    # 给Session设置token
    def set_token(self, url):
        if 'token' not in url:
            raise Exception(f"当前登录的https://mp.weixin.qq.com没有Token")
        Session.token = re.findall(r'token=(\w+)', url)[0]


    # 给Session设置cookie
    def set_cookies(self, driver, cookies):
        Session.cookies = {}
        for item in cookies:
            driver.add_cookie(item)
            Session.cookies[item['name']] = item['value']

    def connect_mongodb(self):
        print('weixindb connecting...')
        try:
            client = pymongo.MongoClient("localhost", 27017)
            self.client = client
            self.db = client.weixindb
            print('weixindb connected')
        except Exception as err:
            print('mongodb connect with error:')
            print(err)


    def close_mongodb(self):
        print('mongodb closing...')
        try:
            self.client.close()
            print('mongodb closed')
        except Exception as err:
            print('mongodb closed with error:')
            print(err)


# for test
def initBizs():
    try:
        client = pymongo.MongoClient("localhost", 27017)
        db = client.weixindb
        fakenames = db.fakenames
        base_dir = os.path.dirname(__file__)
        ac = os.path.join(base_dir, 'fakes/fakenames.txt')
        idx = 0
        if os.path.isfile(ac):
            with open(ac, 'rt') as fi:
                line = fi.readline()
                while line:
                    idx += 1
                    arr = line.strip().split(' ')
                    if len(arr) < 2:
                        arr.append('')
                    fakename = {
                        # 解决诡异的\ufeff
                        'fakename': arr[0].encode('utf-8').decode('utf-8-sig').strip(),
                        'chname': arr[1].encode('utf-8').decode('utf-8-sig').strip()
                    }
                    fakenames.update_one(
                        {'fakename': fakename['fakename']},
                        {"$set": fakename }, True)

                    line = fi.readline()
        else:
            print('err')

        client.close()
    except Exception as err:
        print('mongodb connect with error:')
        print(err)


# 主入口
if __name__ == '__main__':
    print('__main__')
    initBizs()
    Spider().main()
