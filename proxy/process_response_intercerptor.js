const cheerio = require('cheerio')
const redis = require("redis")
const redisClient = redis.createClient()
const { promisify } = require('util');
const redisGetAsync = promisify(redisClient.get).bind(redisClient);
const { ObjectId } = require('mongodb')
const MongoClient = require("mongodb").MongoClient
const mogoUrl = 'mongodb://localhost:27017'
const mongoClient = new MongoClient(mogoUrl)

var inter_home_response = async function (responseDetail) {

    const taskValue = await redisGetAsync('__running_task_')
    if (!taskValue) {
        console.log('- redis中没有进行中的任务')
        return
    }

    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)
    console.log('- responseDetail： ')
    if (responseDetail.response.statusCode != 200) return
    let body_html = responseDetail.response.body.toString('utf8')
    // console.log(body_html)

    // 被ban
    if (body_html.indexOf('操作频繁') > 0) {
        console.log('操作频繁 限制24小时 请更换微信')
        // return
    }

    appmsg_token = body_html.match(/window.appmsg_token = "(.*)"/)[1]
    nickname = body_html.match(/var nickname = "(.*)"/)[1].split('"')[0]
    biz = body_html.match(/var __biz = "(.*)"/)[1]
    pass_ticket = body_html.match(/var pass_ticket = "(.*)"/)[1].split('"')[0]

    console.log('- msgToken ' + appmsg_token)
    const httpid = await redisGetAsync('__running_http_')
    console.log('- httpid ' + httpid)
    await insert_or_update_a_http(httpid, {
        response: body_html,
        appmsg_token,
        nickname,
        taskid: ObjectId(taskid),
        enname,
        biz,
        pass_ticket
    })
}

var inter_s_response = async function (responseDetail) {

    const taskValue = await redisGetAsync('__running_task_') || ''
    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)

    console.log('- responseDetail： ')
    if (responseDetail.response.statusCode != 200) return
    let body_html = responseDetail.response.body.toString('utf8')
    // console.log(body_html)
    const $ = cheerio.load(body_html)
    nickname = $('#js_name').text().trim()
    console.log('- nickname' + nickname)

}


async function insert_or_update_a_http(http_obj_id, datas) {
    http_obj_id = ObjectId(http_obj_id)
    await mongoClient.connect()
    const weixindb = mongoClient.db('weixindb');
    let https = weixindb.collection('https')
    if (!http_obj_id) {
        console.log(' - 无法操作')
    } else {
        return await https.findOneAndUpdate({
            '_id': http_obj_id
        }, {
                '$set': {
                    ...datas
                }
            }, {
                upsert: false
            })
    }

};

module.exports = {
    inter_home_response,
    inter_s_response
}