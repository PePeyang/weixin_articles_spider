import random
import subprocess
import time
import os
from os import system
from new_phone.config import HOME_SEARCH_BUTTON, TOP_BACK_BUTTON_POS, KEY, TOP_DEL_BUTTON_POS, SOU_YI_SOU, GZH_TAB, GZH_ENTRY


class Operate():
    def __init__(self, name):
        # self.connect()
        self.name = name
        pass

    def gen_randomint(self, minIn, maxIn):
        return random.randint(minIn, maxIn)

    def connect(self):
        system('adb kill-server')
        system('adb server')
        outp = system('adb devices')
        print(outp)

    def send_tap(self, position_x, position_y, time_sleep):
        system('adb shell input tap {} {}'.format(position_x, position_y))
        time.sleep(time_sleep)

    def send_fake_swipe(self, start_tap, end_tap, time_dura):
        system('adb shell input swipe {} {} {} {} {}'.format(
            start_tap[0], start_tap[1], end_tap[0], end_tap[1], time_dura))
        time.sleep(0.5)

    def send_name_text(self, name):
        system(('adb shell am broadcast -a ADB_INPUT_TEXT --es msg {}'.format(name)))
        time.sleep(3)

    def home_click(self):
        # x = self.gen_randomint(
        #     HOME_SEARCH_BUTTON['x'][0], HOME_SEARCH_BUTTON['x'][1])
        # y = self.gen_randomint(
        #     HOME_SEARCH_BUTTON['y'][0], HOME_SEARCH_BUTTON['y'][1])
        # self.send_tap(x, y, 0.5)
        # self.send_fake_swipe((150, 300), (150, 599), 500)

        base_dir = os.path.dirname(__file__)
        shellpath = os.path.join(base_dir, 'adbrecord.py')
        # system(b'shellpath')
        # system('adbdo')
        # system('click_search.log')
        # subprocess.call('adbdo', shell=True)


    def search_text(self):
        self.send_name_text(self.name)
        x = self.gen_randomint(
            SOU_YI_SOU['x'][0], SOU_YI_SOU['x'][1])
        y = self.gen_randomint(
            SOU_YI_SOU['x'][0], SOU_YI_SOU['x'][1])
        self.send_tap(x, y, 2)


    def tab_click(self):
        x = self.gen_randomint(
            GZH_TAB['x'][0], GZH_TAB['x'][1])
        y = self.gen_randomint(
            GZH_TAB['y'][0], GZH_TAB['y'][1])
        self.send_tap(x, y, 2)


    def enter_into_gzh(self):
        x = self.gen_randomint(
            GZH_ENTRY['x'][0], GZH_ENTRY['x'][1])
        y = self.gen_randomint(
            GZH_ENTRY['y'][0], GZH_ENTRY['y'][1])
        self.send_tap(x, y, 2)




