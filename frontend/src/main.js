import {createApp} from "vue"
import VueAxios from 'vue-axios'

import App from "./App.vue"
import router from "./router/route"
import axios from "axios";
import md5 from "js-md5"

const md5_password = (password) => {
    let hash = md5.create()
    hash.update(password)
    return hash.hex().toUpperCase()
}

function dateFormat(fmt, date) {
    let ret;
    const opt = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        // 有其他格式化字符需求可以继续添加，必须转化成字符串
    };
    for (let k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length === 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        }
    }
    return fmt;
}


const app = createApp(App);
app.use(router);
app.use(VueAxios, axios);
app.provide("axios", app.config.globalProperties.axios)
app.provide("md5", md5_password)
app.provide("dateFormat", dateFormat)
app.mount("#app");


