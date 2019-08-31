from threading import Thread
import datetime
from process_genbizs import entry

# 一次性从fakenames取出所有的biz
# 构造task数据
# 存入mongodb 发往android

class BIZ_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            entry()
        except BaseException as be:
            print(be)
            self.run()

    def join(self):
        Thread.join(self)


if __name__ == '__main__':
    t = BIZ_THREAD().start()
