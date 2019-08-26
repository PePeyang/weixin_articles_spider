const AnyProxy = require('anyproxy');
const exec = require('child_process').exec;
const { rule } = require('./rule')

// 管理AnyProxy的证书
// AnyProxy.utils.certMgr.ifRootCAFileExists()
// 校验系统内是否存在AnyProxy的根证书
// AnyProxy.utils.certMgr.generateRootCA(callback)
// 生成AnyProxy的rootCA，完成后请引导用户信任.crt文件

// if (!AnyProxy.utils.certMgr.ifRootCAFileExists()) {
//     AnyProxy.utils.certMgr.generateRootCA((error, keyPath) => {
//         // let users to trust this CA before using proxy
//         if (!error) {
//             const certDir = require('path').dirname(keyPath);
//             console.log('NODE_INFO: The cert is generated at', certDir);
//             const isWin = /^win/.test(process.platform);
//             if (isWin) {
//                 exec('start .', { cwd: certDir });
//             } else {
//                 exec('open .', { cwd: certDir });
//             }
//         } else {
//             console.error('NODE_INFO: error when generating rootCA', error);
//         }
//     });
// }

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