import sys
import time
from random import randint
from PhoneControl import OperateAllPhone
from config import BTN, KEY
from VC import VC

class WeixinOperate():
    """
    实现对所有在线手机进行操作 以获取微信请求参数
    """
    busy = 0
    def __init__(self, phone_list):
        self.oap = OperateAllPhone(phone_list)
        # 找一个手机的界面作为眼睛
        self.vc = VC(phone_list[0])

    def home(self):
        """
        :return:通过多次点击BACK按键回到主界面 之所以不直接点击HOME按键 是需要层层返回微信到主界面
        """
        for i in range(8):
            self.oap.key(KEY['BACK_KEYEVENT'])
            time.sleep(0.5)
        return KEY['BACK_KEYEVENT']

    def home_to_gzh_search(self):
        """
        :return:从主界面到公众号搜索
        """
        # 点击微信图标
        self.oap.tap(BTN['EMU_WEIXIN_ICON'])
        time.sleep(2)
        # 点击搜索
        self.oap.tap(BTN['HOME_SEARCH_BUTTON'])
        time.sleep(1)
        return 0

    def search_gzh(self, nickname):
        """
        :param nickname:待搜索公众号名称
        :return:
        """
        # 输入拼音
        self.oap.text(nickname)
        time.sleep(2)
        # 进入账号
        self.oap.tap(BTN['SOU_YI_SOU'])
        time.sleep(5)
        #键入主界面
        self.oap.tap(BTN['GZH_ENTRY'])
        time.sleep(5)
        # 上拉
        self.oap.roll(0,500)
        time.sleep(3)
        return 0

    def all_message(self):
        """
        :return:从公众号主页下拉点击全部消息消息
        """
        # 全部消息
        all_message_pos = self.vc.click_by_words("All Messages",tap=False)
        self.oap.tap(all_message_pos)
        time.sleep(5)
        self.oap.roll(0,500)
        time.sleep(2)
        return 0


    def get_all_req_data(self, nickname, hand=False):
        """
        获取关于一个公众号的全部请求数据 当前程序使用baidu API受到网络和并发限制效果并十分理想
        :param nickname: 公众号昵称
        :return:最后成功与否取决在redis中是否找到有有效数据
        """
        # 回首页
        self.home_to_gzh_search()
        # 搜索公众号
        self.search_gzh(nickname)

        if hand==False:
            self.all_message()
        else:
            input("请一一手动或取参数 回车退出")

        self.home()
