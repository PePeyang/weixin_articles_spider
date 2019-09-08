const AnyProxy = require('anyproxy');
const { rule } = require('./rule')

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


