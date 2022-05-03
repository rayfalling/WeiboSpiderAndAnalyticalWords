<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-layout position="absolute" class="history_content" :native-scrollbar="false">
      <n-space v-if="showEmpty" justify="center" align="center" class="fill_full">
        <n-empty description="还没有浏览记录呢"/>
      </n-space>
      <div v-else>
        <n-list bordered style="position: relative">
          <template #header>
            <n-h1 prefix="bar" align-text style="text-align: center">
              <n-text type="primary">
                浏览记录
              </n-text>
            </n-h1>
          </template>
          <n-list-item v-for="(item, index) in dataList" :item="item" :index="index" :key="item.id">
            <router-link :to="generateUrl(item)" #="{ navigate, href }" custom>
              <n-space justify="space-between" align="center" :wrap="false">
                <n-a tag="div" :underline="false" :href="href" @click="navigate">
                  <div>
                    {{ index + 1 }}
                    <span style="padding-left: 16px">{{ item.content.substr(0, 30) }}...</span>
                  </div>
                </n-a>
                <div>
                  <n-a tag="div" :underline="false" :href="href" @click="navigate">
                    {{ str_time(item.activity_time) }}
                  </n-a>
                  <n-button type="error" style="margin-left: 8px" @click="removeHistory(item.id)">删除</n-button>
                </div>
              </n-space>
            </router-link>
          </n-list-item>
        </n-list>
      </div>
    </n-layout>
  </n-layout>
</template>

<script setup>
import {ref, onMounted, inject} from "vue";
import {useRoute, useRouter} from "vue-router";
import {NLayout, NEmpty, NSpace, NList, NListItem, NText, NH1, NA, NButton, useMessage} from "naive-ui";

import BackgroundImage from "@/components/BackgroundImage";

const dataList = ref([])
const showEmpty = ref(false)

const route = useRoute();
const router = useRouter();
const message = useMessage();

const axios = inject("axios")
const login_status = inject("login")
const dateFormat = inject("dateFormat")

function str_time(time_str) {
  let date = new Date(time_str)
  return dateFormat("YYYY-mm-dd HH:MM:SS", date)
}

function removeHistory(post_id) {
  axios.post("/api/user/history/remove", {
    Username: login_status.value.username,
    PostId: post_id * 1
  }).then(response => {
    if (response.data.status === -1) {
      message.error(response.data.message)
    }
  }).then(() => {
    axios.post("/api/user/history/all", {
      Username: login_status.value.username,
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      dataList.value = response.data.data.result
      showEmpty.value = dataList.value.length === 0
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  })
}

function generateUrl(item) {
  let tag = ""
  let first_index = item.tags.indexOf("#")
  if (first_index !== -1) {
    let second_index = item.tags.indexOf("#", first_index + 1)
    tag = item.tags.substr(first_index + 1, second_index - first_index - 1)
  }

  return "/post/detail/" + item.id + "?keyword=" +
      (item.tags === "" ? item.content.substr(0, 4) : tag) + "&from=history"
}

onMounted(() => {
  let username_local = ""
  if ("username" in route.params) {
    username_local = route.params.username
    axios.post("/api/user/history/all", {
      Username: username_local,
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      dataList.value = response.data.data.result
      showEmpty.value = dataList.value.length === 0
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  }
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

.history_content {
  top: 64px;
  left: 12.5%;
  right: 12.5%;
  height: 80%;
}

@media (min-height: 540px) {
  .history_content {
    top: 64px;
    left: 17.5%;
    right: 17.5%;
    height: 75%;
  }
}

@media (min-height: 960px) {
  .history_content {
    top: 96px;
    left: 22.5%;
    right: 22.5%;
    height: 75%;
  }
}
</style>