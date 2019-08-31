# -*- coding:utf-8 -*-
from threading import Thread
import datetime
from process_suber import suber_entry
from process_adb import adb_entry

class SUBER_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            suber_entry()
        except BaseException as be:
            print(be)
            self.run()

    def join(self):
        Thread.join(self)

class ADB_THREAD (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        try:
            adb_entry()
        except BaseException as be:
            print(be)
            self.run()

    def join(self):
        Thread.join(self)


if __name__ == '__main__':
    # 启动 SUBER_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} SUBER_THREAD 启动中...'.format(bftime))
    t1 = SUBER_THREAD()
    t1.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} SUBER_THREAD 已启动'.format(aftime))

    # 启动 ADB_THREAD
    bftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 启动中...'.format(bftime))
    t2 = ADB_THREAD()
    t2.start()
    aftime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print('- {} ADB_THREAD 已启动'.format(aftime))


