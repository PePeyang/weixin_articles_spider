const url = require('url')
const querystring = require('querystring');

var interest_url = {
  "load_more": "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",        //更多历史消息
  "getappmsgext": "https://mp.weixin.qq.com/mp/getappmsgext?",                //阅读消息
  "appmsg_comment": "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment",//评论信息
  "content": "https://mp.weixin.qq.com/s?",                                       //文章正文html
}

var fake_url = {
  "geticon": "https://mp.weixin.qq.com/mp/geticon?",
  "getappmsgext":"https://mp.weixin.qq.com/mp/getappmsgext?"
}

var normal_url = {
  "home": "https://mp.weixin.qq.com/mp/profile_ext?action=home",
  "getmsg": "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",
  "article": "https://mp.weixin.qq.com/s?"
}

function sendToRedis(key, value) {
  var redis = require("redis");
  client = redis.createClient(6379, 'localhost', {});
  client.on("error", function (err) {
    console.log("NODE_INFO: error:")
    console.log(err)
    console.log("NODE_INFO: 有可能是redis尚未启动...")
  });
  client.set(key, value, 'EX', 60 * 60 * 24);
  client.quit();
};

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
          let key = FAKE_PREFIX + urlName + '_' + timestamp + '_biz=' + biz + '_REQUEST'
          let value = {
            REQUEST_URL,
            REQUEST_PROTOCOL,
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
          let key = FAKE_PREFIX + urlName + '_' + timestamp + '_biz=' + biz + '_REQUEST'
          let value = {
            REQUEST_URL,
            REQUEST_PROTOCOL,
            REQUEST_HEADERS,
            REQUEST_COOKIE,
            REQUEST_DATA: rd_str,
            pass_ticket
          }
          sendToRedis(key, JSON.stringify(value))
        }

        return true
      }
    })

    // return signArr.indexOf(true) > -1

  },
  // 发送响应前处理
  *beforeSendResponse(requestDetail, responseDetail) {
    // ANCHOR  不通过anyproxy了
    // if (requestDetail.url.includes("https://mp.weixin.qq.com/mp/profile_ext?action=home")) {
    //   var body_str = responseDetail.response.body.toString('utf8')
    //   if (body_str.includes('操作频繁')) {
    //     console.log('NODE_INFO: 操作频繁 限制24小时 请更换微信')
    //     body_str = body_str.replace('操作频繁，请稍后再试', 'Sotyoyo 提示：操作频繁 限制24小时 请更换微信')
    //     responseDetail.response.body = Buffer(body_str)
    //   }
    //   else {
    //     // TODO fix appmsg_token 的提取方法，太low了
    //     var data = body_str.split('window.appmsg_token = "')
    //     var appmsg_token = data[1].split('"')[0]
    //     sendToRedis(NORMAL_PREFIX + 'appmsg_token', appmsg_token)
    //   }
    // }
  },
  *beforeDealHttpsRequest(requestDetail) {
    return true
  },
  *onError(requestDetail, error) { /* ... */ },
  *onConnectError(requestDetail, error) { /* ... */ }
};

module.exports ={
  rule
}