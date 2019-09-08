# -*- coding:utf-8 -*-
import time
import sys
import signal
from threading import Thread
import datetime
from process_adb import adb_entry
from process_listen import listen_task_entry


class ADB_THREAD(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        adb_entry()

    def join(self):
        Thread.join(self)


class LITEN_TASK_THREAD(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        listen_task_entry()

    def join(self):
        Thread.join(self)

if __name__ == '__main__':
    # 启动 LITEN_TASK_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 启动中...'.format(bftime))
    t_listen = LITEN_TASK_THREAD()
    t_listen.daemon = True
    t_listen.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} LITEN_TASK_THREAD 已启动'.format(aftime))

    # 启动 ADB_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 启动中...'.format(bftime))
    t_adb = ADB_THREAD()
    t_adb.daemon = True
    t_adb.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 已启动'.format(aftime))

    while True:
        time.sleep(2)
