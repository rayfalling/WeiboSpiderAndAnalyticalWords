<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-space vertical align="center">
      <SearchInput class="search_content" width="560px" @on-search-clicked="onSearch" :content="keyword"/>
      <n-layout position="absolute" class="list_content" :native-scrollbar="false">
        <n-space v-if="showEmpty" justify="center" align="center" class="fill_full">
          <n-empty description="什么也没有搜索到"/>
        </n-space>
        <div v-else>
          <n-list bordered>
            <template #header>
              <n-h1 prefix="bar" align-text style="text-align: center">
                <n-text type="primary">
                  相关资讯
                </n-text>
              </n-h1>
            </template>
            <n-list-item v-for="(item, index) in dataList" :item="item" :index="index" :key="item.id">
              <router-link :to="'/post/detail/' + item.id + '?keyword=' + keyword" #="{ navigate, href }" custom>
                <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                  <n-a tag="div" :underline="false" :href="href" @click="navigate">
                    <div>
                      {{ index + 1 }}
                      <span style="padding-left: 16px">{{ spilt_content(item.content) }}</span>
                      <span v-if="item.tags.length !== 0" style="padding-left: 16px">{{ item.tags }}</span>
                    </div>
                  </n-a>
                  <div>
                    <n-a tag="div" :underline="false" :href="href" @click="navigate">
                      {{ str_time(item.time) }}
                    </n-a>
                    <n-button v-if="isAdmin" type="error" style="margin-left: 8px" @click="removePost(item.id)">
                      删除
                    </n-button>
                  </div>
                </n-space>
              </router-link>
            </n-list-item>
          </n-list>
        </div>
      </n-layout>
    </n-space>
  </n-layout>
</template>

<script setup>
import {ref, onMounted, inject} from "vue";
import {onBeforeRouteUpdate, useRoute, useRouter} from "vue-router";
import {NLayout, NEmpty, NSpace, NList, NListItem, NText, NH1, NA, NButton, useMessage} from "naive-ui";

import SearchInput from "@/components/SearchInput";
import BackgroundImage from "@/components/BackgroundImage";

const route = useRoute();
const router = useRouter();
const message = useMessage();

const axios = inject("axios")
const isAdmin = inject("isAdmin")
const dateFormat = inject("dateFormat")

const showEmpty = ref(false)
const keyword = ref(null)
const dataList = ref([])

const onSearch = word => {
  if (word == null || word === "") {
    message.error("搜索内容为空")
  } else {
    // jump to search page
    router.push({path: "/search", query: {keyword: word}})
  }
}

const removePost = (post_id) => {
  axios.post("/api/admin/post/delete", {
    PostId: post_id
  }).then(response => {
    if (response.data.status === -1) {
      message.error("删除失败")
    } else {
      message.info("删除成功")
      querySearch()
    }
  }).catch(err => {
    if (err.response.status === 401) {
      router.push({path: "/login"})
    }
  })
}

function str_time(time_str) {
  let date = new Date(time_str)
  return dateFormat("YYYY-mm-dd HH:MM:SS", date)
}

function spilt_content(content) {
  if (content.length >= 30) {
    return content.substr(0, 30) + "..."
  }
  return content
}

function querySearch() {
  axios.post("/api/search", {Keyword: keyword.value}).then(response => {
    dataList.value = response.data.data.result
    showEmpty.value = response.data.data.result.length === 0
  }).catch(err => {
    if (err.response.status === 401) {
      router.push({path: "/login"})
    }
  })
}

onMounted(() => {
  if ("keyword" in route.query) {
    keyword.value = route.query.keyword
    querySearch()
  } else {
    message.error("搜索关键词为空")
  }
})

onBeforeRouteUpdate(to => {
  if ("keyword" in to.query) {
    keyword.value = to.query.keyword
    querySearch()
  } else {
    message.error("搜索关键词为空")
  }
});
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

.search_content {
  margin-top: 32px;
  width: 480px;
}

.list_content {
  top: 108px;
  left: 12.5%;
  right: 12.5%;
  height: 60%;
}

@media (min-height: 540px) {
  .list_content {
    top: 108px;
    left: 17.5%;
    right: 17.5%;
    height: calc(80% - 32px);
  }
}

@media (min-height: 960px) {
  .list_content {
    top: 108px;
    left: 22.5%;
    right: 22.5%;
    height: 80%;
  }
}
</style>

<!--suppress CssUnusedSymbol -->
<style>
.n-list.n-list--bordered {
  border: 0;
}
</style>
