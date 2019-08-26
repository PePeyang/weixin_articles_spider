var interest_url = {
  "load_more": "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg",        //更多历史消息
  "getappmsgext": "https://mp.weixin.qq.com/mp/getappmsgext?",                //阅读消息
  "appmsg_comment": "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment",//评论信息
  "content": "https://mp.weixin.qq.com/s?",                                       //文章正文html
}

function sendToRedis(key, value) {
  var redis = require("redis");
  client = redis.createClient(6379, 'localhost', {});
  client.on("error", function (err) {
    console.log("NODE_INFO: error:" + err);
    console.log("NODE_INFO: 有可能是redis尚未启动...")
  });
  client.set(key, value, 'EX', 60 * 60 * 24);
  client.quit();
};

const rule = {
  // 模块介绍
  summary: 'my customized rule for AnyProxy',
  // 发送请求前拦截处理
  *beforeSendRequest(requestDetail) {
    // 每一请求的关键信息
    var data_needed = {}
    data_needed['protocol'] = requestDetail.protocol
    data_needed['url'] = requestDetail.url
    data_needed['requestOptions'] = requestDetail.requestOptions
    // data_needed['requestData'] = requestDetail.requestData
    // 请求的url感兴趣就保存本次请求的信息到文件中
    // console.log(`- 详情 ${data_needed['url']}`)

    let signArr = Object.keys(interest_url).map((urlName) => {
      if (data_needed['url'].includes(interest_url[urlName])) {
        console.log(`- 代理https成功 ${data_needed['url']}`)
        let rd_buf = Buffer(requestDetail.requestData)
        let rd_str = rd_buf.toString('utf8')
        data_needed['requestData'] = rd_str
        let timestamp = Date.now().toString()
        let key = timestamp + '.' + interest_url[urlName] + '.req'
        let value = JSON.stringify(data_needed)
        sendToRedis(key, value)
        return true
      }
    })

    // return signArr.indexOf(true) > -1

  },
  // 发送响应前处理
  *beforeSendResponse(requestDetail, responseDetail) {
    if (requestDetail.url.includes(interest_url.getappmsgext)) {
      var body_str = responseDetail.response.body.toString('utf8')
      body_json = JSON.parse(body_str)
      // console.log(body_json)
      // console.log(requestDetail)

      // 这是我的昵称。。。搞了半天
      var nick_name = body_json.nick_name
      var wxuin = undefined
      console.log(`NODE_INFO: ${requestDetail.requestOptions.headers}`)
      cookie = requestDetail.requestOptions.headers.Cookie
      // console.log(`NODE_INFO: ${cookie}`)
      cookie_arr = cookie.split('; ')
      for (item in cookie_arr) {
        if (cookie_arr[item].includes("wxuin")) {
          wxuin = cookie_arr[item].split('=')[1]
          break
        }
      }
      console.log(`NODE_INFO: nick_name=${nick_name} wxuin=${wxuin}`)
      if (wxuin != undefined) {
        sendToRedis(nick_name + '.nick_name', wxuin)
      }
    }
    if (requestDetail.url.includes("https://mp.weixin.qq.com/mp/profile_ext?action=home")) {
      var body_str = responseDetail.response.body.toString('utf8')
      if (body_str.includes('操作频繁')) {
        console.log('NODE_INFO: 操作频繁 限制24小时 请更换微信')
        body_str = body_str.replace('NODE_INFO: 操作频繁，请稍后再试', 'AII提示：操作频繁 限制24小时 请更换微信')
        responseDetail.response.body = Buffer(body_str)
      }
      else {
        var data = body_str.split('var nickname = "')
        var current_nickname = data[1].split('" || ""')[0]
        sendToRedis('current_nickname', current_nickname)
      }
    }
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