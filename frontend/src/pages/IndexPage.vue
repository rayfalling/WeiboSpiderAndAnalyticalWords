<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-space justify="space-between" align="center" class="full_page">
      <div></div>
      <n-space vertical justify="space-between" align="center">
        <SearchInput width="480px" @on-search-clicked="onSearch"/>
        <n-space v-if="isAdmin()" justify="space-between" align="center" style="width: 480px">
          <n-input v-model:value="spider_key" style="width: 180px" type="text" round size="small"
                   placeholder="请输入爬取关键词"/>
          <n-input v-model:value="spider_pages" style="width: 180px" type="text" round size="small"
                   placeholder="请输入爬取页数"/>
          <n-button :loading="loading" size="small" round type="primary" @click="onSpider">更新</n-button>
        </n-space>
      </n-space>
      <div></div>
    </n-space>
  </n-layout>
</template>

<script setup>
import {ref, inject, onMounted} from "vue";
import {useRouter} from "vue-router";
import {NLayout, NSpace, NInput, NButton, useMessage} from "naive-ui";

import SearchInput from "@/components/SearchInput";
import BackgroundImage from "@/components/BackgroundImage";

const loading = ref(false)
const spider_key = ref(null)
const spider_pages = ref(null)

const router = useRouter();
const message = useMessage();

const axios = inject("axios")
const isAdmin = inject("isAdmin")

const onSpider = () => {
  if (loading.value)
    return

  loading.value = true
  axios.post("/api/admin/spider/update", {
    Keyword: spider_key.value,
    Pages: spider_pages.value * 1
  }).then(response => {
    if (response.data.status === -1) {
      message.error(response.data.message)
    } else {
      message.info("爬取数据成功, 共" + response.data.data.spider_count + "条")
    }
    loading.value = false
  }).catch(() => loading.value = false)
}

const onSearch = keyword => {
  if (keyword == null || keyword === "") {
    message.error("搜索内容为空")
  } else {
    // jump to search page
    router.push({path: "/search", query: {keyword: keyword}})
  }
}

onMounted(() => {
  axios.post("/api/login/status").then(response => {
    if (response.data.status === -1) {
      router.push({path: "/login"})
    }
  })
});
</script>

<style scoped>
.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}
</style>