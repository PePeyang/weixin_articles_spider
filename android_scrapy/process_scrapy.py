from scrapy import cmdline

def start_scrapy_home():
    cmdline.execute('scrapy crawl HomeSpider'.split())



def start_scrapy_loads():
    cmdline.execute('scrapy crawl LoadsSpider'.split())
