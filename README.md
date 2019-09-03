## 微信公众号爬虫项目
### 运行环境
### 技术支持
### 运行原理

![运行原理](./assets/运行机制.png)

1. proxy.js监控api信息，抓取两条api的数据进入redis
2. run main 守护进程，
> 当redis内数据有变化时候 先拿出来与数据库现有数据比对，
- 如果找到一致的，那就把类cookie信息覆盖进去 然后取出来使用
- 如果没找到，drop出来 存入数据库。加上公众号的一些信息存进去，设置offset为0
3. 拿到当前的信息后，可以执行伪造请求，
> 伪造的home请求内容可以暂存入redis
> 抓取到的最终清洗过得数据存入mongodb
4.
### QUICK START

1. 先运行proxy线程

2. 再运行android线程

3. 再运行biz线程


### 联系方式
> wechat: 18921966826
### 项目架构TODO
1. redis内存数据库，加快数据库读写效率
2. hbase分布式数据库存储，用来解决大数据量
3. 分布式爬取，todo with scrapy-redis
4. 构建web项目，更友好的操作洁面
5. 权限体系，包月服务等收费措施

### FAQ （frequently asked questions ）
> 为什么要使用redis做消息队列
- 首先是因为有生产者消费者设计模式的必要，其次是因为js线程和python线程之间，python线程和python线程之间需要通信，所以依赖了redis

> 为什么要用wechat 6.6.7
- 7.0+ 官方对反爬虫做了一些应对措施，操作起来比较困难
- 6.7.3 这个因人而异可能 我用的genymotion模拟器 ROM6 下打开微信操作的时候会一直有莫名的报错
- 6.5.8 有个查看历史按钮 位置不固定 其他都很固定
- 6.6.7 不错，基本满足我的要求