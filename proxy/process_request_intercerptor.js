const url = require('url')
const querystring = require('querystring')
const { ObjectId } = require('mongodb')
const MongoClient = require("mongodb").MongoClient
const mogoUrl = 'mongodb://localhost:27017'
const mongoClient = new MongoClient(mogoUrl)

const assert = require('assert')
const redis = require("redis")
const redisClient = redis.createClient()
const { promisify } = require('util');
const redisGetAsync = promisify(redisClient.get).bind(redisClient);

const FAKE_PREFIX = '__fake_'
const NORMAL_PREFIX = '__normal_'

var inter_gethome_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie
    const rd_buf = Buffer(requestDetail.requestData)
    const rd_str = rd_buf.toString('utf8')

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = params.__biz;

    const taskValue = await redisGetAsync('__running_task_')
    if (!taskValue) {
        console.log('- redis中没有进行中的任务')
        return
    }

    let value = {
        biz,
        REQUEST_URL,
        REQUEST_COOKIE,
        REQUEST_HEADERS,
        REQUEST_DATA: rd_str
    }

    let http = await insert_or_update_a_http(null, value, 'actionhome')
    await redisClient.set('__running_http_', http.insertedId.toString())
}

var inter_geticon_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

    const taskValue = await redisGetAsync('__running_task_')
    if (!taskValue) {
        console.log('- redis中没有进行中的任务')
        return
    }

    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)
    let rd_buf = Buffer(requestDetail.requestData)
    let rd_str = rd_buf.toString('utf8')

    console.log(`- 开始采集请求信息 ${REQUEST_URL}`)
    console.log(`- url TYPE INFO: geticon`)

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = params.__biz;
    let key = FAKE_PREFIX + 'geticon_biz=' + biz + '_REQUEST'
    let value = {
        REQUEST_URL,
        REQUEST_COOKIE,
        REQUEST_HEADERS,
        REQUEST_DATA: rd_str
    }

    /**
     * 有没有大神给我解决一个问题。。。 头都炸了
     * 问题描述：
     * 现在需要再proxy中抓取两条api 他们的先后顺序不确定，但是两条的数据都要拿到
     * 数据库需要维护每一次任务对应的这两条http请求数据
     * 另外 redis set数据好像不能同步执行
     */

    let http = await insert_or_update_a_http(ObjectId('111111111111'), value, 'geticon')

    // const httpValue = await redisGetAsync('__running_http_')
    // if (!httpValue) {
    //     let http = await insert_or_update_a_http(null, value, 'geticon')
    //     console.log(`- httpid: ${http.insertedId}`)
    //     if (!ObjectId.isValid(httpValue)) {
    //         await redisClient.set('__running_http_', http.insertedId)
    //     }
    // } else {
    //     console.log(`- httpValue ${httpValue}`)
    //     let http = insert_or_update_a_http(ObjectId(httpValue), value, 'geticon')
    //     await redisClient.del('__running_http_')
    // }

}

var inter_getmsg_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

    const taskValue = await redisGetAsync('__running_task_')
    console.log(taskValue)
    if (!taskValue) {
        console.log('- redis中没有进行中的任务')
        return
    }

    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)
    let rd_buf = Buffer(requestDetail.requestData)
    let rd_str = rd_buf.toString('utf8')

    console.log(`- 开始采集请求信息 ${REQUEST_URL}`)
    console.log(`- url TYPE INFO: getappmsgext`)

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = querystring.parse(rd_str).__biz
    let key = FAKE_PREFIX + 'getappmsgext_biz=' + biz + '_REQUEST'
    let value = {
        REQUEST_URL,
        REQUEST_HEADERS,
        REQUEST_COOKIE,
        REQUEST_DATA: rd_str,
    }

    let http = await insert_or_update_a_http(ObjectId('111111111111'), value, 'getappmsgext')
    // const httpValue = await redisGetAsync('__running_http_')
    // if (!httpValue) {
    //     let http = await insert_or_update_a_http(null, value, 'getappmsgext')
    //     // console.log(`- http: `)
    //     // console.log(http)
    //     console.log(`- httpid: ${http.insertedId}`)
    //     if (!ObjectId.isValid(httpValue)) {
    //         await redisClient.set('__running_http_', http.insertedId)
    //     }

    // } else {
    //     console.log(`- httpValue ${httpValue}`)
    //     let http = insert_or_update_a_http(ObjectId(httpValue), value, 'geticon')
    //     await redisClient.del('__running_http_')
    // }
}



async function insert_or_update_a_http(http_obj_id, value, key) {
    await mongoClient.connect()
    const weixindb = mongoClient.db('weixindb');

    let https = weixindb.collection('https')
    if (!http_obj_id) {
        return await https.insertOne({
            [key]: value
        })
    } else {
        return await https.findOneAndUpdate({
            '_id': http_obj_id
        }, {
            '$set': {
                [key]: value
            }
        }, {
            upsert: true
        })
    }

};

// async function get_biz_by_name(name) {
//     console.log("Connected successfully to server");
//     const db = mongoClient.db('weixindb');
//     let biznames = db.collection('biznames')
//     biznames.findOne({ 'chname': name }, function (err, res) {
//         console.log(res)
//         return res
//     })
// }

module.exports = {
    inter_geticon_request,
    inter_getmsg_request,
    inter_gethome_request
}