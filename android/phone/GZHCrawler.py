from .WeixinOperate import WeixinOperate
import os


class GZHCrawler():
    """
    只有一个实例对象，在设计模式中可以采用单例模式
    接受一个公众号爬虫管理者实例作为参数
    """
    def __init__(self, enname):
        print('GZHCrawler __init__')
        self.enname = enname

    def run(self):
        """
        :return:新加入的爬虫每当接到文章爬取任务时就会自动获取请求参数
        公众号爬虫的整个生命周期中都需要有一个后台进程监控公众的的爬取任务和更新任务
        run需要在一个进程中不停执行
        """
        print('gc running')
        deviceInfo = self.connectDevcie()

        if deviceInfo:
            ADB_PORT = deviceInfo
            wo = WeixinOperate([ADB_PORT])
            wo.get_all_req_data(self.enname, hand=False)
        else:
            print('无连接设备！')

    def connectDevcie(self):
        '''检查设备是否连接成功，如果成功返回True，否则返回False'''
        '''获取设备列表信息，并用"\r\n"拆分'''
        result = os.popen('adb devices')
        res = result.read()
        deviceInfo = ''
        for line in res.splitlines():
            print(line)
            if '5555' in line:
                deviceInfo = line.split('\t')[0]
        '''如果没有链接设备或者设备读取失败，第二个元素为空'''
        if deviceInfo == '':
            return False
        else:
            return deviceInfo
