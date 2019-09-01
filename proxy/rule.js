const url = require('url')
const querystring = require('querystring');
const { inter_geticon_request, inter_getmsg_request } = require('./process_request_intercerptor')
const { inter_s_response } = require('./process_response_intercerptor')

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
    beforeSendRequest: async function beforeSendRequest(requestDetail) {
        const REQUEST_URL = requestDetail.url
        if (REQUEST_URL.includes(fake_url.geticon)) {
            await inter_geticon_request(requestDetail)
        } else if (REQUEST_URL.includes(fake_url.getappmsgext)){
            await inter_getmsg_request(requestDetail)
        }

    },
    // 发送响应前处理
    beforeSendResponse: async function beforeSendResponse(requestDetail, responseDetail) {
        const REQUEST_URL = requestDetail.url
        if (REQUEST_URL.includes(normal_url.article)) {
            await inter_s_response(responseDetail)
        }
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