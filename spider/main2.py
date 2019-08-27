from Application.gzh_crawler import GZHCrawler
from ui.ui_instance import app, socketio, the_redis
# from Application.gzh_category import GZHCategory

# 公众号爬虫应用实例
gc = GZHCrawler()
# 公众号类别管理实例 主要服务于定向搜索
# gzh_category = GZHCategory()

def run_gzh_crawler():
    import time
    while True:
        # 增加时间等待防止CPU使用率过高
        time.sleep(1)
        gc.run()