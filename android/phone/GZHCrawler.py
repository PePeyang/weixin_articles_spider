from .WeixinOperate import WeixinOperate
# from auth import ADB_PORT
ADB_PORT = '192.168.58.108:5555'


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

        wo = WeixinOperate([ADB_PORT])
        wo.get_all_req_data(self.enname, hand=False)
