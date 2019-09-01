const url = require('url')
const querystring = require('querystring')
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

var inter_geticon_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

    const taskValue = await redisGetAsync('__running_task_') || ''
    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)
    let rd_buf = Buffer(requestDetail.requestData)
    let rd_str = rd_buf.toString('utf8')

    console.log(`- 开始采集请求信息 ${REQUEST_URL}`)
    console.log(`- url TYPE INFO: ${urlName}`)

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = params.__biz;
    let key = FAKE_PREFIX + urlName + '_biz=' + biz + '_REQUEST'
    let value = {
        REQUEST_URL,
        REQUEST_COOKIE,
        REQUEST_HEADERS,
        REQUEST_DATA: rd_str
    }

    let httpid = sendToMongodb(value)
}

var inter_getmsg_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie

    const taskValue = await redisGetAsync('__running_task_') || ''
    let taskid = taskValue.split('_between_')[0]
    let enname = taskValue.split('_between_')[1]
    console.log(`- taskid: ${taskid} enname: ${enname}`)
    let rd_buf = Buffer(requestDetail.requestData)
    let rd_str = rd_buf.toString('utf8')

    console.log(`- 开始采集请求信息 ${REQUEST_URL}`)
    console.log(`- url TYPE INFO: ${urlName}`)

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = querystring.parse(rd_str).__biz
    let key = FAKE_PREFIX + urlName + '_biz=' + biz + '_REQUEST'
    let value = {
        REQUEST_URL,
        REQUEST_HEADERS,
        REQUEST_COOKIE,
        REQUEST_DATA: rd_str,
    }
    sendToMongodb(value)

}

function doPublish() {
    client.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    client.publish('there_is_a_http', '2222222xxxxxxxxx22222222')
}

function sendToRedis(key, value) {
    redisClient.on("error", function (err) {
        console.log(err)
        console.log("NODE_INFO: 有可能是redis尚未启动...")
    });
    // 设置十分钟的有效期 因为geticon有效期差不多就这么多
    redisClient.set(key, value, 'EX', 60 * 10 * 60);
};

function sendToMongodb(value) {


};

function get_biz_by_name(name) {
    mongoClient.connect(function (err) {
        assert.equal(null, err);
        console.log("Connected successfully to server");
        const db = mongoClient.db('weixindb');
        let biznames = db.collection('biznames')

        biznames.findOne({ 'chname': name }, function (err, res) {
            console.log(res)

            return res
        })

    });
}

module.exports = {
    inter_geticon_request,
    inter_getmsg_request
}