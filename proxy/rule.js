const url = require('url')
const querystring = require('querystring');

const fake_url = {
    "geticon": "https://mp.weixin.qq.com/mp/geticon?",
    "getappmsgext": "https://mp.weixin.qq.com/mp/getappmsgext?"
}

const normal_url = {
    "home": "https://mp.weixin.qq.com/mp/profile_ext?action=home",
    // "load_more": "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",      //更多历史消息
    "getmsg": "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",
    // "comment": "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment", //评论信息
    "article": "https://mp.weixin.qq.com/s?"
}

function sendToRedis(key, value) {
    var redis = require("redis");
    client = redis.createClient(6379, 'localhost', {});
    client.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    // 设置十分钟的有效期 因为geticon有效期差不多就这么多
    client.set(key, value, 'EX', 60 * 10 * 60);
    client.quit();
};

function doPublish(){
    var redis = require("redis");
    client = redis.createClient(6379, 'localhost', {});
    client.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    client.publish('spider', '有新的公众号了')
    client.quit();
}

const FAKE_PREFIX = '__fake_'
const NORMAL_PREFIX = '__normal_'

const rule = {
    // 模块介绍
    summary: '微信公众号爬虫',
    // 发送请求前拦截处理
    *beforeSendRequest(requestDetail) {
        const REQUEST_URL = requestDetail.url
        const REQUEST_PROTOCOL = requestDetail.protocol
        const REQUEST_HEADERS = requestDetail.requestOptions.headers
        const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

        let timestamp = Date.now().toString()

        let signArr = Object.keys(fake_url).map((urlName) => {
            if (REQUEST_URL.includes(fake_url[urlName])) {
                let rd_buf = Buffer(requestDetail.requestData)
                let rd_str = rd_buf.toString('utf8')

                console.log(`- 开始采集请求信息 ${REQUEST_URL}`)
                console.log(`- url TYPE INFO: ${urlName}`)

                if (urlName === 'geticon') {
                    let temp_url = url.parse(REQUEST_URL);
                    let params = querystring.parse(temp_url.query)
                    let biz = params.__biz;
                    let key = FAKE_PREFIX + urlName + '_biz=' + biz + '_REQUEST'
                    let value = {
                        REQUEST_URL,
                        REQUEST_COOKIE,
                        REQUEST_HEADERS
                    }
                    sendToRedis(key, JSON.stringify(value))
                }

                if (urlName === 'getappmsgext') {
                    let temp_url = url.parse(REQUEST_URL);
                    let params = querystring.parse(temp_url.query)
                    let biz = querystring.parse(rd_str).__biz
                    let pass_ticket = params.pass_ticket;
                    let key = FAKE_PREFIX + urlName + '_biz=' + biz + '_REQUEST'
                    let value = {
                        REQUEST_URL,
                        REQUEST_HEADERS,
                        REQUEST_COOKIE,
                        REQUEST_DATA: rd_str,
                        // pass_ticket
                    }
                    sendToRedis(key, JSON.stringify(value))
                }

                return true
            }
        })

        if (signArr.indexOf(true) > -1) {
            doPublish()
        }
    },
    // 发送响应前处理
    *beforeSendResponse(requestDetail, responseDetail) { },
    *beforeDealHttpsRequest(requestDetail) {
        return true
    },
    *onError(requestDetail, error) { /* ... */ },
    *onConnectError(requestDetail, error) { /* ... */ }
};

module.exports = {
    rule
}