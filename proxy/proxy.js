const AnyProxy = require('anyproxy');
const redis = require('redis')
const { rule } = require('./rule')


// function sendToRedis(key, value) {
//     client = redis.createClient();
//     client.on("error", function (err) {
//         console.log(err)
//         console.log("NODE_INFO: 有可能是redis尚未启动...")
//     });
//     // 设置十分钟的有效期
//     client.set(key, value, 'EX', 60 * 10);
//     client.quit();
// };


// function suberServer() {
//     sub = redis.createClient()

//     sub.subscribe('there_is_a_adb', function () {
//         sub.on('message', function (chan, msg) {
//             console.log(`- 订阅到来自 ${chan} 的消息: `)
//             let taskid = msg.match(/__taskid_(.*)/g)[0]
//             sendToRedis()
//             console.log(taskid)
//         }
//         )
//     })
//     sub.quit();
// }
// suberServer()

// 例如，设置一个 key 并设置 10s 超时
// function TestKey() {
//     pub = redis.createClient()
//     pub.set('there_is_a_test', 'redis notify-keyspace-events : expired')
//     pub.expire('there_is_a_test', 10)
//     pub.quit()
// }

// function keyExpired(e, r) {
//     // 如果key过期 那就把那个task status 设置为失败
//     sub = redis.createClient()
//     const expired_subKey = `__keyevent@0__:expired`
//     sub.subscribe(expired_subKey, function () {
//         console.log(' - Subscribed to "' + expired_subKey + '" event channel : ' + r)
//         sub.on('message', function (channel, msg) {
//             console.log(` - ${channel} [expired] ${msg} `)
//         })
//         // TestKey()
//     })
// }

// function pubServer()  {
//     pub = redis.createClient()
//     pub.send_command('config', ['set', 'notify-keyspace-events', 'Ex'], keyExpired)
//     pub.quit();
// }

// pubServer()

const options = {
    port: 8001,
    rule: rule,
    webInterface: {
        enable: true,
        webPort: 8002
    },
    throttle: 10000,
    forceProxyHttps: true,
    wsIntercept: false, // 不开启websocket代理
    silent: false
};
const proxyServer = new AnyProxy.ProxyServer(options);

proxyServer.on('ready', () => { /* */ });
proxyServer.on('error', (e) => {
    console.log(e)
});
proxyServer.start();


