// K 键空间通知，所有通知以 keyspace@ 为前缀，针对Key
// E 键事件通知，所有通知以 keyevent@ 为前缀，针对event
// x 过期事件：每当有过期键被删除时发送
// e 驱逐(evict)事件：每当有键因为 maxmemory 政策而被删除时发送

var redis = require('redis'),
    RDS_PORT = 6379,//端口号
    RDS_HOST = '127.0.0.1', //服务器IP
    RDS_OPTS = {},//设置项
    puber = redis.createClient(RDS_PORT, RDS_HOST, RDS_OPTS);


pub.send_command('config', ['set', 'notify-keyspace-events', 'Ex'], subscribeExpired)
/**


**/