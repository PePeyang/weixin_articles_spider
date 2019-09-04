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

    const taskid = await redisGetAsync('__running_task_')
    if (!taskid) {
        console.log('- redis中没有进行中的任务')
        return
    }

    await mongoClient.connect()
    const weixindb = mongoClient.db('weixindb');
    let tasks = weixindb.collection('tasks')
    let running_task = await tasks.findOne({ '_id': ObjectId(taskid)})
    console.log(running_task)
    let enname = running_task.task_biz_enname
    // mongoClient.quit()
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

    let appmsg_token = body_html.match(/window.appmsg_token = "(.*)"/)[1]
    let nickname = body_html.match(/var nickname = "(.*)"/)[1].split('"')[0]
    let biz = body_html.match(/var __biz = "(.*)"/)[1]
    let pass_ticket = body_html.match(/var pass_ticket = "(.*)"/)[1].split('"')[0]

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


async function insert_or_update_a_http(http_obj_id, datas) {
    http_obj_id = ObjectId(http_obj_id)
    await mongoClient.connect()
    const weixindb = mongoClient.db('weixindb');
    let https = weixindb.collection('https')
    return await https.findOneAndUpdate(
        {
        '_id': http_obj_id
        },
        {
            '$set': {
                ...datas
            }
        },
        {
            upsert: true,
            returnNewDocument: true
        }
    )
};

module.exports = {
    inter_home_response
}