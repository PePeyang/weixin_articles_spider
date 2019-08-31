class FakeHomeParams:
    cookies = {
        'rewardsn': '',
        'wxuin': '3604431997', # cover
        'devicetype': 'android-23',
        'version': '27000634',  # cover
        'lang': 'zh_CN',
        'pass_ticket': '',  # cover
        'wap_sid2': '',  # cover
        'wxtokenkey': '777',
    }

    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools',
        'x-wechat-uin': '',  # cover
        'x-wechat-key': '',  # cover
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.tencent.mm',
    }

    params = (
        ('action', 'home'),
        ('__biz', ''),  # cover
        ('devicetype', 'android-23'),
        ('version', '27000634'),  # cover
        ('lang', 'zh_CN'),
        ('nettype', 'WIFI'),
        ('a8scene', '7'),
        ('session_us', 'gh_9e26999263b5'),  # cover or not
        ('pass_ticket', ''),  # cover
        ('wx_header', '1'),
    )
