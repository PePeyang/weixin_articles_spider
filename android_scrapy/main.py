import sys
from threading import Thread
import datetime
import signal
from process_listen import listen_http_entry
from process_scrapy import start_scrapy_home
from scrapy import cmdline

class LITEN_TASK_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            listen_http_entry()
        except Exception as e:
            print(e)
            self.run()

    def join(self):
        Thread.join(self)


# def quit(signum, frame):
#     print('----手动停止-----')
#     sys.exit()
#     sys.exit()


if __name__ == '__main__':
    # signal.signal(signal.SIGINT, quit)
    # signal.signal(signal.SIGTERM, quit)

    # 启动 LITEN_TASK_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 启动中...'.format(bftime))
    t_listen = LITEN_TASK_THREAD()
    t_listen.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 已启动'.format(aftime))


    start_scrapy_home()