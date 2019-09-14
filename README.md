## 微信公众号爬虫项目 （开发不易，请点star，让我知道你曾经来过！🥳）
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

> gemymotion [https://www.genymotion.com/]
收费软件，但是有试用一个月 [https://www.genymotion.com/fun-zone/] 这个链接进去点下载，然后注册帐号操作
- Custom Phone Api 8.0 （一定要下载安装 Android Api 为 8.0 的）
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

语言描述运行逻辑（回复issue）

1. 第一步，是将配置的.conf文件内写入的公众号使用python加入到mongodb数据库bizs中，这一步是即时操作的，也就是一次性完成，基本不存在延迟。然后会再读取一遍数据库中的bizs，生成相应任务模式的对应tasks，并且把这些tasks加入redis中的TASKS_QUEUE中，此时这些task的状态都为generated。（生成任务，可在后续改造成使用web api的方式，这样就具备了很好的拓展性）
2. 第二步，启动anyproxy的代理，为的是截获当程序真正运行起来时候的几条关键性api，拦截下来的token，appmsgtoken，cookie等信息，会写入数据库，并且将该条http在数据库中的id存入redis，表示正在运行中的任务的http信息，当然，这一步会把第三步描述的taskid也存入，这样他俩就关联起来了。
3. 第三步，启动一个线程，轮询redis中的__running_task_ 当redis中没有运行中的任务，就在TASKS_QUEUE队列中pop一条出来，状态设为running_in_adb，并且设入__running_task_中，且发布一条消息there_is_a_task，用来通知模拟器有任务进行了。这样就意味着有任务在运行了，注意，一次只能有一个任务在运行。
4. 第四步，同样启动一个线程，订阅there_is_a_task，如果收到了通知，那么就会执行GZHCrawler这个实例，按照设定好的步骤自动操作安卓机器。且改变redis中任务的状态为running_in_adb。
5. 回到了第二步，这里在adb操作进行中的时候就会监听到http请求，当有满足符合要求的请求时，改变redis中这条任务的状态为running_in_http。且发布一条消息there_is_a_http。
6. 第五步，启动scrapy爬虫（其实这一步要在第三步之前启动，只是这里用来描述运行逻辑，所以写在这里了）爬虫订阅到了消息there_is_a_http，就运行 `scrapy crawl LoadSpider`把之前拦截的关键内容构造成请求历史文章接口的api，丢给scrapy去执行，并且将结果存储到数据库loads。这一步完成后，任务状态就变成了end_success
7. 第七步，等到第六步彻底结束，运行另一个scrapy爬虫，`scrapy crawl ArticleSpider` 这一步可以彻底把所有的loads爬取成最后文章的html和图片存入本地文件夹output中

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

- 用到了蘑菇代理...这个是收费的，别想了，我一会就把它重置掉😒。。。配置文件在 `/weixin_articles_spider/android_scrapy/android_scrapy/settings.py` 这里面，这里不是建议使用蘑菇代理，用别家代理记得改代理中间件的逻辑，希望大家帮我修缮一下也不错，提高代理ip的复用率

- 应该还有许多地方我暂时没想到的，后补


### 欢迎PR，仅供学习使用，如自行使用产生法律纠纷，与本人无关
