<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-layout>
      <NavBar></NavBar>
      <n-layout style="height: calc(100vh - 72px)" has-sider>
        <router-view class="view"/>
      </n-layout>
    </n-layout>
  </n-config-provider>
</template>

<script setup>
import NavBar from "@/components/NavBar"
import {NLayout, NConfigProvider} from "naive-ui";

const themeOverrides = {
  Layout: {
    colorEmbedded: "#F0F0F5"
  },
}
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
