<template>
  <n-layout-header style="height: 72px; padding: 8px 24px; width: 100%" bordered>
    <n-space justify="space-between" align="center">
      <div style="width: 320px; text-align: left">
        <n-space align="center" size="large">
          <n-image width="48" :src="require('@/assets/logo.png')" preview-disabled/>
          <n-button style="font-size: 1.25rem" dashed tag="a" strong size="large" @click="onIndex">
            首页
          </n-button>
        </n-space>
      </div>
      <div style="width: 320px">
        <n-space justify="space-around" align="center" size="large">
          <router-link to="/" #="{ navigate, href }" custom>
            <n-button style="font-size: 1.25rem" dashed tag="a" strong size="large">
              企业热榜
            </n-button>
          </router-link>
          <router-link to="/" #="{ navigate, href }" custom>
            <n-button style="font-size: 1.25rem" dashed tag="a" strong size="large">
              最新动态
            </n-button>
          </router-link>
        </n-space>
      </div>
      <div style="width: 320px; text-align: right">
        <router-link to="/" #="{ navigate, href }" custom>
          <n-button style="font-size: 1.25rem" dashed tag="a" strong size="large" @click="rightButtonClick">
            {{ rightButtonText }}
          </n-button>
        </router-link>
      </div>
    </n-space>
  </n-layout-header>
</template>

<script setup>
import {useRoute, useRouter} from "vue-router"
import {ref, watch, inject, onMounted} from "vue";
import {NSpace, NImage, NButton, NLayoutHeader} from "naive-ui";

let jumpUrl = "/login"
const rightButtonText = ref("登录");

const route = useRoute()
const router = useRouter()

const axios = inject('axios');
const login_status = inject("login")

const onIndex = () => {
  router.push({path: "/"})
}

const rightButtonClick = () => {
  router.push({path: jumpUrl})
}

onMounted(() => {
  axios.post("/api/login/status").then(response => {
    if (response.data.status === 0) {
      login_status.value.login = true
      login_status.value.username = response.data.data.username
      login_status.value.nickname = response.data.data.nickname
      login_status.value.user_type = response.data.data.user_type
    }

    update(route.fullPath)
  })
});

function update(path) {
  if (path === "/login") {
    rightButtonText.value = "注册";
    jumpUrl = "/register";
  } else if (path === "/register") {
    rightButtonText.value = "登录";
    jumpUrl = "/login";
  } else if (login_status.value.login) {
    rightButtonText.value = "我的";
    jumpUrl = "/user/" + login_status.value.username;
  }
}

update(route.fullPath);

watch(
    () => route.fullPath,
    path => {
      // TODO 登录态
      if (path === "/login") {
        rightButtonText.value = "注册";
        jumpUrl = "/register";
      } else if (path === "/register") {
        rightButtonText.value = "登录";
        jumpUrl = "/login";
      } else if (login_status.value.login) {
        rightButtonText.value = "我的";
        jumpUrl = "/user/" + login_status.value.username;
      }
    }
)
</script>

<style scoped>

</style>