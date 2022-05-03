<template>
  <n-message-provider>
    <n-config-provider :theme-overrides="themeOverrides">
      <n-layout>
        <NavBar></NavBar>
        <n-layout style="height: calc(100vh - 72px)" has-sider>
          <router-view class="view"/>
        </n-layout>
      </n-layout>
    </n-config-provider>
  </n-message-provider>
</template>

<script setup>
import {ref, provide} from "vue";
import {NLayout, NConfigProvider, NMessageProvider} from "naive-ui";

import NavBar from "@/components/NavBar"

const themeOverrides = {
  Layout: {
    colorEmbedded: "#F0F0F5"
  },
  Divider: {
    color: "#CFCFCF"
  },
  List: {
    borderColor: "#CECECE"
  }
}

const login_status = ref({
  login: false,

  avatar: "",
  username: "",
  nickname: "",
  user_type: 1,
})

const isAdmin = () => {
  return login_status.value.user_type === 0
}

provide("isAdmin", isAdmin)
provide("login", login_status)
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100%;
  height: 100%;
}
</style>
