## 微信公众号爬虫项目
![scrapy](./assets/title.jpg)
### 这是个什么东东（前言）
#### 使用python制作的爬虫，用来爬取微信公众号内的文章。
#### 相信仔细研究过得同学，会发现市面上的几种思路的缺点：
  1. 利用https://weixin.sogou.com 微信搜狗进行爬取
  -  爬取到的文章不全，很多遗漏的
  2. 利用https://mp.weixin.qq.com 创作稿件，搜索对应模板
  - 微信公众号帐号代价昂贵，且大概在50页请求后就会被ban
#### 我的思路
通过对手机微信客户端的请求抓包，获取到访问历史文章的分页接口，批量生产 🥳
最大的好处，可实现大量的微信公众号之间的切换，且只要你微信足够多，爬多少都不是问题
### 运行环境(windows/mac)

> gemymotion(3.0.2)[https://www.genymotion.com/]
收费软件，但是有试用一个月
- Custom Phone Api 8.0
- ARM_Translation_Oreo
- wechat 6.7.3
- ARM_Translation_Oreo和wechat 6.7.3下载地址：
链接: https://pan.baidu.com/s/1iPoWR9QH-LBL2tX2Gp5Mug 提取码: t6wg
> virtualbox(6.0.x) gemymotion自带

> jdk 1.6+

> android platform-tools
- adb 1.0.26

> nodejs 8.16.1
- anyproxy

> python 3.6.8

- pymongo 3.9.0
- redis 3.3.8
- scrapy 1.7.3
- baidu-aip
    `pip install baidu-aip`
- Pillow 6.1.x
- numpy 1.17.x

> mongodb 4.0.12

> redis 3

整体的环境配置比较复杂，所以需要有一定的基础才可以配置成功
### 技术支持
scrapy
![scrapy](./assets/scrapy_architecture.png)

### 运行原理
执行机制
![执行机制](./assets/project_process.png)

### QUICK START
#### genymotion配置
1. 官网下载，安装，登录自己的帐号，下载对应的模拟器 Custom Phone Api 8.0
2. 打开模拟器，设置adb路径为自己安装的adb路径，将ARM_Translation_Oreo拖入其中，点OK，再点OK (adb怎么安装的google一下)
3. 使用adb重启模拟器 `adb shell reboot`
4. 等待机器完全重启，使用adb安装weixin.6.7.3 `adb install ~/Downloads/weixin6.7.3.apk` (路径自己根据系统微调)
5. 全局安装一下anyproxy, 然后根据官网指示[http://anyproxy.io] 把ssl证书装好，模拟器上的证书别忘记装（先设置pin密码，再通过anyproxy代理，然后下载root.crt安装）
PS：比较难操作，过几天放操作的gif吧
6. 搞定了以后把微信打开，把待测试的微信登录上去，然后点下面的返回按钮一层一层返回到桌面（重要，不是废操作不然我也不会写这么多字）
#### 启动redis （这个我不需要写了吧😉）-何况写起来还挺麻烦的
#### 启动mongodb （这个我不需要写了吧😉）-何况写起来还挺麻烦的
#### 启动proxy
```
$ cd /weixin_articles_spider/proxy
$ npm install
$ node proxy.js
```
#### 设置自己想爬的公众号
```bash
$ cd /weixin_articles_spider/assets
# 修改 fakenames.conf 按照里面一模一样的格式改哦，一行一个、中间一个空格隔开、不要留有空行、id在前
$ cd /weixin_articles_spider/biz
$ python main.py
# 等执行完了这里可以ctrl+c退出
```
#### 运行scrapy 进入待爬取状态
```bash
$ cd /weixin_articles_spider/android_scrapy
$ python main.py
# 不要做任何退出动作
```
#### 再运行android操作的任务
```bash
$ cd /weixin_articles_spider/android
$ python main.py
# 不要做任何退出动作
```
#### 等待结果
- 如果在上一步操作之后不久，你看到你得模拟器上的微信开始动起来了，那就说明您已经基本成功了。
- 接下来就是等待爬取完成，这个过程取决于你提供的微信公众号数量多少，不要提供超过30个，否则很快就会被ban哦。每一个公众号大概耗时4分钟左右，目前设置的模式是爬取最新的十条文章。
- 等待6-7分钟如果模拟器不动了，那就说明爬取完成，之后：
    ```bash
    $ cd /weixin_articles_spider/android_scrapy
    $ scrapy crawl ArticleSpider
    # 等待执行结束后去 /weixin_articles_spider/android_scrapy/output 就有结果了
    ```


### 联系方式
> wechat: Sotyoyo  
> issues请直接在github提出，微信只用来交友或者商务、内推我就业（前端开发🥺）
### 项目架构TODO
1. 分布式数据库存储，用来解决大数据量
2. 构建web项目，更友好的操作界面
3. 消息通知机制，爬取完成自动邮件通知

### FAQ （frequently asked questions ）
> 为什么要使用redis做消息队列
- 首先是因为有生产者消费者设计模式的必要，其次是因为js线程和python线程之间，python线程和python线程之间需要通信，所以依赖了redis

> 为什么要用wechat 6.7.3
- 7.0+ 官方对反爬虫做了一些应对措施，操作起来比较困难
- 6.7.3 这个因人而异 需要使用高版本ROM
- 6.5.8 有个查看历史按钮 位置不固定 其他都很固定
- 6.6.7 不错，基本满足我的要求 但是后来发现这个也会被提示强制升级

> ban是什么意思？
- 打游戏的时候会有一种模式叫BP模式，ban（禁用）/ pick（挑选）模式哦！🤓

### 注意
项目的配置文件主要在 /weixin_articles_spider/configs/auth.py，但是由于本人技术问题，遗留了一些数据库配置在别处😅，不过问题不大，，一般不用改。

值得一提的是，
- 用到了百度API的图像文字识别，这部分配置在auth.py可修改，我暂时不把我自己申请的移除，有需要的同学请去(百度ai)[https://ai.baidu.com/tech/ocr/general] 自取。

- 用到了蘑菇代理...这个是收费的，别想了，我一会就把它重置掉😒。。。配置文件在 `/weixin_articles_spider/android_scrapy/android_scrapy/settings.py` 这里面

- 应该还有许多地方我暂时没想到的，后补


### 欢迎PR，仅供学习使用，如自行使用产生法律纠纷，与本人无关
