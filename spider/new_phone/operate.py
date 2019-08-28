import random
from os import system
from new_phone.config import HOME_SEARCH_BUTTON, TOP_BACK_BUTTON_POS, KEY, TOP_DEL_BUTTON_POS, SOU_YI_SOU, GZH_TAB, GZH_ENTRY


class Operate():
    def __init__(self):
        # self.connect()
        pass

    def gen_randomint(self, minIn, maxIn):
        return random.randint(minIn, maxIn)

    def connect(self):
        system('adb kill-server')
        system('adb server')
        outp = system('adb devices')
        print(outp)

    def send_tap(self, position_x, position_y):
        system('adb shell input tap {} {}'.format(position_x, position_y))

    def home_click(self):
        x = self.gen_randomint(
            HOME_SEARCH_BUTTON['x'][0], HOME_SEARCH_BUTTON['x'][1])
        y = self.gen_randomint(
            HOME_SEARCH_BUTTON['y'][0], HOME_SEARCH_BUTTON['y'][1])
        self.send_tap(x, y)






