# -*- coding:utf-8 -*-
import signal
import sys
from process_adb import adb_entry
from process_suber import suber_entry
from process_listen import listen_task_entry
from threading import Thread
import datetime

class SUBER_THREAD (Thread):
    def __init__(self, queue):
        self.queue = queue
        Thread.__init__(self)

    def run(self):
        suber_entry(self.queue)

    def join(self):
        Thread.join(self)

class ADB_THREAD (Thread):
    def __init__(self, queue):
        Thread.__init__(self)

    def run(self):
        adb_entry()

    def join(self):
        Thread.join(self)

class LITEN_TASK_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        listen_task_entry()

    def join(self):
        Thread.join(self)


def quit(signum, frame):
    print('----手动停止-----')
    sys.exit()
    sys.exit()

if __name__ == '__main__':

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    # 启动 LITEN_TASK_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 启动中...'.format(bftime))
    t_listen = LITEN_TASK_THREAD()
    t_listen.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 已启动'.format(aftime))

    # # 启动 SUBER_THREAD
    # bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    # print('- {} SUBER_THREAD 启动中...'.format(bftime))
    # t1 = SUBER_THREAD()
    # t1.start()
    # aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    # print('- {} SUBER_THREAD 已启动'.format(aftime))

    # 启动 ADB_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 启动中...'.format(bftime))
    t2 = ADB_THREAD()
    t2.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 已启动'.format(aftime))


