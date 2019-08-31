const redis = require('redis')
const CONF = { db: 3 }

let pub, sub

// Activate "notify-keyspace-events" for expired type events
pub = redis.createClient(CONF)
pub.send_command('config', ['set', 'notify-keyspace-events', 'Ex'], subscribeExpired)

// Subscribe to the "notify-keyspace-events" channel used for expired type events
function subscribeExpired(e, r) {
    sub = redis.createClient(CONF)
    const expired_subKey = `__keyevent@${CONF.db}__:expired`

    sub.subscribe(expired_subKey, function () {
        console.log(' [i] Subscribed to "' + expired_subKey + '" event channel : ' + r)
        sub.on('message', function (chan, msg) {
            console.log('[expired]', msg)
        }
        )
        TestKey()
    })
}

//例如，设置一个 key 并设置 10s 超时
function TestKey() {
    pub.set('testing', 'redis notify-keyspace-events : expired')
    pub.expire('testing', 10)
}