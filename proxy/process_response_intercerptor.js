const cheerio = require('cheerio')
const redis = require("redis")
const redisClient = redis.createClient()
const { promisify } = require('util');
const redisGetAsync = promisify(redisClient.get).bind(redisClient);

var inter_s_response = async function (responseDetail) {

    const taskValue = await redisGetAsync('__running_task_')
    console.log(taskValue)

    // client.get('__running_task_', function (err, taskValue) {
    //     if (err || !taskValue) return
    //     let taskid = taskValue.split('_between_')[0]
    //     let enname = taskValue.split('_between_')[1]
    //     if (REQUEST_URL.includes(normal_url['article'])) {
    //         console.log('- responseDetail： ')
    //         if (responseDetail.response.statusCode != 200) return
    //         let body_html = responseDetail.response.body.toString('utf8')
    //         // console.log(body_html)
    //         const $ = cheerio.load(body_html)
    //         nickname = $('#js_name').text().trim()
    //         console.log('- nickname' + nickname)

    //     }
    // })
}


module.exports = {
    inter_s_response
}