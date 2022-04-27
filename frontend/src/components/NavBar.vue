<template>
  <n-layout-header style="height: 72px; padding: 8px 24px; width: 100%" bordered>
    <n-space justify="space-between" align="center">
      <div style="width: 160px; text-align: left">
        <n-image width="48" :src="require('@/assets/logo.png')" preview-disabled/>
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
      <div style="width: 160px; text-align: right">
        <router-link to="/" #="{ navigate, href }" custom>
          <n-button style="font-size: 1.25rem" dashed tag="a" strong size="large">
            返回首页
          </n-button>
        </router-link>
      </div>
    </n-space>
  </n-layout-header>
</template>

<script setup>
import {NSpace, NImage, NButton, NLayoutHeader} from "naive-ui";

</script>

<style scoped>

</style>