const cheerio = require('cheerio')
const redis = require("redis")
const redisClient = redis.createClient()
const { promisify } = require('util');
const redisGetAsync = promisify(redisClient.get).bind(redisClient);

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

module.exports = {
    inter_s_response
}