const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        port: 8080,
        https: false,
        open: false,
        proxy: {
            "/api": {
                target: "http://127.0.0.1:8088", //设置调用的接口域名和端口
                changeOrigin: true, //是否跨域
                ws: true,
            },
            "/static": {
                target: "http://127.0.0.1:8088",
                changeOrigin: true,
            }
        }
    }
})
