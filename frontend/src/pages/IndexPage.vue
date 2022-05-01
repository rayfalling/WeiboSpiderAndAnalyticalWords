<template>
  <n-layout embedded class="full_page">
    <BackgroundImage />
    <n-space justify="space-between" align="center" class="full_page">
      <div></div>
      <SearchInput width="480px" @on-search-clicked="onSearch"/>
      <div></div>
    </n-space>
  </n-layout>
</template>

<script setup>
import {inject, onMounted} from "vue";
import {useRouter} from "vue-router";
import {NLayout, NSpace, useMessage} from "naive-ui";

import SearchInput from "@/components/SearchInput";
import BackgroundImage from "@/components/BackgroundImage";

const router = useRouter();
const message = useMessage();
const axios = inject("axios")

const onSearch = keyword => {
  if (keyword == null || keyword === "") {
    message.error("搜索内容为空")
  } else {
    // jump to search page
    router.push({path: "/search", query:{keyword: keyword}})
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