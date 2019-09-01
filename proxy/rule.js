const url = require('url')
const querystring = require('querystring');
const cheerio = require('cheerio')
const MongoClient = require("mongodb").MongoClient
const mogoUrl = 'mongodb://localhost:27017'
const mongoClient = new MongoClient(mogoUrl);
const assert = require('assert');

const redis = require("redis");
const client = redis.createClient();

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
    client.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    // 设置十分钟的有效期 因为geticon有效期差不多就这么多
    client.set(key, value, 'EX', 60 * 10 * 60);
};

function sendToMongodb(value) {


};

function get_biz_by_name(name) {
    mongoClient.connect(function (err) {
        assert.equal(null, err);
        console.log("Connected successfully to server");
        const db = mongoClient.db('weixindb');
        let biznames = db.collection('biznames')

        biznames.findOne({'chname': name}, function(err, res){
            console.log(res)

            return res
        })

    });
}

function doPublish(){
    client.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    client.publish('there_is_a_http', '2222222xxxxxxxxx22222222')
}

const FAKE_PREFIX = '__fake_'
const NORMAL_PREFIX = '__normal_'

const rule = {
    // 模块介绍
    summary: '微信公众号爬虫',
    // 发送请求前拦截处理
    *beforeSendRequest(requestDetail) {
        const REQUEST_URL = requestDetail.url
        const REQUEST_HEADERS = requestDetail.requestOptions.headers
        const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

        let timestamp = Date.now().toString()

        client.get('__running_task_', function (err, taskValue) {
            if (err || !taskValue) return
            console.log(taskValue)
            let taskid = taskValue.split('_between_')[0]
            let enname = taskValue.split('_between_')[1]
            let httpid = ''
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
                        sendToMongodb(value)
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
                        sendToMongodb(value)
                    }


                }
            })

            if (signArr.filter(e => e).length > 1) doPublish(taskid, httpid)

        })

    },
    // 发送响应前处理
    *beforeSendResponse(requestDetail, responseDetail) {
        const REQUEST_URL = requestDetail.url

        client.get('__running_task_', function (err, taskValue) {
            if (err || !taskValue) return
            let taskid = taskValue.split('_between_')[0]
            let enname = taskValue.split('_between_')[1]
            if (REQUEST_URL.includes(normal_url['article'])) {
                console.log('- responseDetail： ')
                if (responseDetail.response.statusCode != 200) return
                let body_html = responseDetail.response.body.toString('utf8')
                // console.log(body_html)
                const $ = cheerio.load(body_html)
                nickname = $('#js_name').text().trim()
                console.log('- nickname' + nickname)

            }
        })
    },
    *beforeDealHttpsRequest(requestDetail) {
        return true
    },
    *onError(requestDetail, error) { /* ... */ },
    *onConnectError(requestDetail, error) { /* ... */ }
};

module.exports = {
    rule
}