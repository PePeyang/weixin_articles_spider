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

    def join(self):
        Thread.join(self)



class Thread_2 (Thread):
    def __init__(self, rqlist):
        Thread.__init__(self)
        self.rqlist = rqlist

    def run(self):
        try:
            data_crawler(self.rqlist)
        except BaseException as e:
            print(e)
            self.run()

    def join(self):
        Thread.join(self)


class Thread_3 (Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        phone_operator()


if __name__ == '__main__':
    rqlist = RQ('_redis_queue_')
    # t1 = Thread_1(rqlist).start()
    t2 = Thread_2(rqlist).start()
    # t3 = Thread_3().start()

