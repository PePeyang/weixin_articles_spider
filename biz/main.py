import sys
import time
from threading import Thread
import datetime
import signal
from process_genbizs import entry


class BIZ_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        entry()

    def join(self):
        Thread.join(self)


if __name__ == '__main__':

    # 启动 BIZ_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 启动中...'.format(bftime))
    t = BIZ_THREAD()
    t.daemon = True
    t.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} BIZ_THREAD 已启动'.format(aftime))


    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("优雅的手动停止...")
        sys.exit(1)
