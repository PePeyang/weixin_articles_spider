import sys
from threading import Thread
import datetime
import signal
from process_genbizs import entry

class BIZ_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            entry()
        except BaseException as be:
            print(be)
            # self.run()

    def join(self):
        Thread.join(self)


def quit(signum, frame):
    print('----手动停止-----')
    sys.exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    # 启动 BIZ_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 启动中...'.format(bftime))
    t = BIZ_THREAD()
    t.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 已启动'.format(aftime))
    t.join()
    fftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 已结束'.format(fftime))


