import {createApp} from "vue"
import VueAxios from 'vue-axios'

import App from "./App.vue"
import router from "./router/route"
import axios from "axios";

const app = createApp(App);
app.use(router);
app.use(VueAxios, axios);
app.provide("axios", app.config.globalProperties.axios)
app.mount("#app");
