<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-layout position="absolute" class="trend_content" :native-scrollbar="false">
      <n-space v-if="showEmpty" justify="center" align="center" class="fill_full">
        <n-empty description="什么也没有搜索到"/>
      </n-space>
      <div v-else>
        <n-list bordered style="position: relative">
            <template #header>
              <n-h1 prefix="bar" align-text style="text-align: center">
                <n-text type="primary">
                  企业热缩
                </n-text>
              </n-h1>
            </template>
            <n-list-item v-for="(item, index) in dataList" :item="item" :index="index" :key="item.id">
              <router-link :to="'/search?keyword=' + item.tags" #="{ navigate, href }" custom>
                <n-a tag="div" :underline="false" :href="href" @click="navigate">
                  <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                    <div>
                      {{ index + 1 }}
                      <span style="padding-left: 16px">#{{ item.tags }}#</span>
                    </div>
                    <div style="padding-left: 16px">{{ item.trend }}</div>
                  </n-space>
                </n-a>
              </router-link>
            </n-list-item>
        </n-list>
      </div>
    </n-layout>
  </n-layout>
</template>

<script setup>
import {ref, onMounted, inject} from "vue";
import {useRouter} from "vue-router";
import {NLayout, NEmpty, NSpace, NList, NListItem, NText, NH1, NA} from "naive-ui";

import BackgroundImage from "@/components/BackgroundImage";

const dataList = ref([])
const showEmpty = ref(false)

const router = useRouter();

const axios = inject("axios")

function queryTrend() {
  axios.post("/api/post/trend").then(response => {
    dataList.value = response.data.data.result.slice(0, 9)
    showEmpty.value = dataList.value.length === 0
  }).catch(err => {
    if (err.response.status === 401) {
      router.push({path: "/login"})
    }
  })
}

onMounted(() => {
  queryTrend()
})
</script>

<style scoped>
a {
  text-decoration: none;
}

.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}

.fill_full {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.trend_content {
  top: 64px;
  left: 12.5%;
  right: 12.5%;
  height: 80%;
}

@media (min-height: 540px) {
  .trend_content {
    top: 64px;
    left: 17.5%;
    right: 17.5%;
    height: 75%;
  }
}

@media (min-height: 960px) {
  .trend_content {
    top: 64px;
    left: 22.5%;
    right: 22.5%;
    height: 65%;
  }
}
</style>