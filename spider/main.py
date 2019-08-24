# -*- coding: utf-8 -*-
# TODO 自定义类
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import re
import shutil
import os
import json
import argparse
import traceback
import random
import math
import codecs
import datetime
import lxml

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


def main():
    # /usr/bin/chromedriver
    chrome = input('请输入chromedriver路径 (注意要和自己的chrome版本匹配):').strip()
    if not chrome:
        if os.path.isfile('chromedriver'):
            chrome = 'chromedriver'
        else:
            print('没有合适的chromedriver，程序无法进行！')
            return

    driver = webdriver.Chrome(executable_path=chrome)
    print('Succeed to load driver')
    do_weixin_login(driver)
    return
    # cookies = json.load(open('cookies.json', 'rb')
    #                     ) if os.path.isfile('cookies.json') else []
    # driver.get(Urls.index)

# 微信首页的登陆
def do_weixin_login(driver):
    if not driver:
        print('Are you kidding me ？没有driver玩毛线')
        return

    cookies = json.load(open('caches/cookies.json', 'rb')
                        ) if os.path.isfile('caches/cookies.json') else []
    driver.get(Urls.index)
    if not cookies:
        # TODO 自动输入账号密码 给出二维码然后自动登陆 只需要自己扫个码
        # ANCHOR cookie一般一天就到期
        input("请先手动登录, 完成后按回车继续:")
        cookies = driver.get_cookies()
        open('caches/cookies.json', 'wb').write(json.dumps(cookies).encode('utf-8'))
    set_cookies(driver, cookies)
    return

# 给driver设置cookie
def set_cookies(driver, cookies):
      Session.cookies = {}
      for item in cookies:
          driver.add_cookie(item)
          Session.cookies[item['name']] = item['value']


# 主入口
if __name__ == '__main__':
    print('__main__')
    main()
