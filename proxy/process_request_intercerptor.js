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

var inter_gethome_request = async function (requestDetail) {
    const REQUEST_URL = requestDetail.url
    const REQUEST_HEADERS = requestDetail.requestOptions.headers
    const REQUEST_COOKIE = REQUEST_HEADERS.Cookie
    const rd_buf = Buffer(requestDetail.requestData)
    const rd_str = rd_buf.toString('utf8')

    let temp_url = url.parse(REQUEST_URL);
    let params = querystring.parse(temp_url.query)
    let biz = params.__biz;

    const taskid = await redisGetAsync('__running_task_')
    if (!taskid) {
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

    await set_task_mongodb_status(taskid, 'running_in_http')
}

async function insert_or_update_a_http(http_obj_id, value, key) {
    await mongoClient.connect()
    // TODO config
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

async function set_task_mongodb_status(taskid, status) {
    let task_obj_id = ObjectId(taskid)
    await mongoClient.connect()
    // TODO config
    const weixindb = mongoClient.db('weixindb');
    let tasks = await weixindb.collection('tasks')
    await tasks.findOneAndUpdate(
        { '_id': task_obj_id },
        {
            '$set': {
                'task_status': status,
                'task_updatetime': Date.now().toLocaleString()
            }
        })
}


module.exports = {
    inter_gethome_request
}