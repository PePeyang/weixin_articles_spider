from tools.data_queue import RQ
from threading import Thread
from applications import proxy_listener, data_crawler, phone_operator
import datetime


class Thread_1 (Thread):
    def __init__(self, rqlist):
        Thread.__init__(self)
        self.rqlist = rqlist

    def run(self):
        proxy_listener(self.rqlist)


class Thread_2 (Thread):
    def __init__(self, rqlist):
        Thread.__init__(self)
        self.rqlist = rqlist

    def run(self):
        data_crawler(self.rqlist)


class Thread_3 (Thread):
    def __init__(self, rqlist):
        Thread.__init__(self)
        self.rqlist = rqlist

    def run(self):
        phone_operator(self.rqlist)


if __name__ == '__main__':
    rqlist = RQ('_redis_queue_')
    # t1 = Thread_1(rqlist).start()
    t2 = Thread_2(rqlist).start()
    t3 = Thread_3(rqlist).start()











