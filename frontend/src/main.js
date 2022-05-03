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

const app = createApp(App);
app.use(router);
app.use(VueAxios, axios);
app.provide("axios", app.config.globalProperties.axios)
app.provide("md5", md5_password)
app.mount("#app");


