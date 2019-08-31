from threading import Thread
import datetime
from process_genbizs import entry

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
    # 启动 BIZ_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 启动中...'.format(bftime))
    t = BIZ_THREAD().start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 已结束'.format(aftime))