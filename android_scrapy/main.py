import sys
from threading import Thread
import datetime
from process_scrapy import start_scrapy_loads
from scrapy import cmdline

# def quit(signum, frame):
#     print('----手动停止-----')
#     sys.exit()
#     sys.exit()


if __name__ == '__main__':
    # signal.signal(signal.SIGINT, quit)
    # signal.signal(signal.SIGTERM, quit)

    start_scrapy_loads()
