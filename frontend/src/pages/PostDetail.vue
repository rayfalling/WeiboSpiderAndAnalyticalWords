<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-space vertical align="center" justify="center" style="position: relative">
      <div class="content_row">
        <n-space justify="center" align="center">
          <div class="card_block detail">
            <n-card hoverable :title="post_detail.tags" content-style="padding: 0 8px 8px 8px;" style="height: 100%"
                    header-style="text-align: center; font-size: 1.5rem; padding: 16px 16px 8px 16px" size="medium">
              <template #header-extra>
                <n-button @click="goBack">
                  返回列表
                </n-button>
              </template>
              <div class="card_content">
                <n-space vertical justify="space-between" style="height: 100%">
                  <div style="padding: 8px">
                    <n-space justify="end" align="center">
                      <span style="font-size: 1rem">{{ post_detail.username }}</span>
                      <span style="font-size: 1rem">{{ post_detail.time }}</span>
                    </n-space>
                    <p style="padding: 0 2rem">{{ post_detail.content }}</p>
                  </div>
                  <n-space justify="space-between" style="height: 100%">
                    <div style="width: 120px;"></div>
                    <n-space justify="center" align="center">
                      <div>
                        <n-icon size="24" style="vertical-align: middle">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path
                                d="M352.92 80C288 80 256 144 256 144s-32-64-96.92-64c-52.76 0-94.54 44.14-95.08 96.81c-1.1
                          109.33 86.73 187.08 183 252.42a16 16 0 0 0 18 0c96.26-65.34 184.09-143.09
                          183-252.42c-.54-52.67-42.32-96.81-95.08-96.81z"
                                fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                stroke-width="32">
                            </path>
                          </svg>
                        </n-icon>
                        <span class="icon_font">{{ post_detail.attitudes_count }}</span>
                      </div>
                      <div>
                        <n-icon size="24" style="vertical-align: middle">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
                            <path d="M573 421c-23.1 0-41 17.9-41 40s17.9 40 41 40c21.1 0 39-17.9 39-40s-17.9-40-39-40zm-280
                        0c-23.1 0-41 17.9-41 40s17.9 40 41 40c21.1 0 39-17.9 39-40s-17.9-40-39-40z" fill="currentColor">
                            </path>
                            <path d="M894 345c-48.1-66-115.3-110.1-189-130v.1c-17.1-19-36.4-36.5-58-52.1c-163.7-119-393.5-82.7-513
                        81c-96.3 133-92.2 311.9 6 439l.8 132.6c0 3.2.5 6.4 1.5 9.4c5.3 16.9 23.3 26.2 40.1 20.9L309 806c33.5
                         11.9 68.1 18.7 102.5 20.6l-.5.4c89.1 64.9 205.9 84.4 313 49l127.1 41.4c3.2 1 6.5 1.6 9.9 1.6c17.7 0
                          32-14.3 32-32V753c88.1-119.6 90.4-284.9 1-408zM323
                          735l-12-5l-99 31l-1-104l-8-9c-84.6-103.2-90.2-251.9-11-361c96.4-132.2 281.2-161.4 413-66c132.2
                           96.1 161.5 280.6 66 412c-80.1 109.9-223.5 150.5-348 102zm505-17l-8 10l1 104l-98-33l-12 5c-56
                            20.8-115.7 22.5-171 7l-.2-.1C613.7 788.2 680.7 742.2 729 676c76.4-105.3
                             88.8-237.6 44.4-350.4l.6.4c23 16.5 44.1 37.1 62 62c72.6 99.6 68.5 235.2-8 330z"
                                  fill="currentColor">
                            </path>
                            <path d="M433 421c-23.1 0-41 17.9-41 40s17.9 40 41 40c21.1 0 39-17.9 39-40s-17.9-40-39-40z"
                                  fill="currentColor">
                            </path>
                          </svg>
                        </n-icon>
                        <span class="icon_font">{{ post_detail.comments_count }}</span>
                      </div>
                      <div>
                        <n-icon size="24" style="vertical-align: middle">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                            <path d="M13.33 12.838l4.497-4.423l.057-.065a.587.587 0 0 0-.057-.767L13.33
                         3.162l-.062-.053c-.36-.27-.89-.01-.89.469v2.13l-.225.015c-3.563.282-5.65 2.537-6.148
                         6.627c-.064.525.538.854.928.506c1.431-1.278 2.91-2.072
                         4.445-2.39c.246-.051.493-.09.742-.117l.258-.023v2.096l.005.082c.06.453.609.666.947.334zM12.226
                          6.72l1.152-.077V4.61l3.446 3.388l-3.446 3.39V9.231l-1.356.122h-.008c-1.703.183-3.31.865-4.827
                          2.002c.298-1.339.807-2.346 1.476-3.067c.83-.895 1.99-1.443 3.563-1.569zM5.5 4A2.5 2.5 0 0 0 3
                           6.5v8A2.5 2.5 0 0 0 5.5 17h8a2.5 2.5 0 0 0 2.5-2.5v-1a.5.5 0 0 0-1 0v1a1.5 1.5 0 0 1-1.5
                           1.5h-8A1.5 1.5 0 0 1 4 14.5v-8A1.5 1.5 0 0 1 5.5 5h3a.5.5 0 0 0 0-1h-3z" fill="currentColor">
                            </path>
                          </svg>
                        </n-icon>
                        <span class="icon_font">{{ post_detail.reposts_count }}</span>
                      </div>
                    </n-space>
                    <div>
                      <n-button icon-placement="left" type="primary" dashed @click="switchCollectStatus">
                        <template #icon>
                          <n-icon v-if="collectStatus" size="20" style="vertical-align: middle">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19
                              8.63L2 9.24l5.46 4.73L5.82 21z" fill="currentColor"></path>
                            </svg>
                          </n-icon>
                          <n-icon v-else size="20" style="vertical-align: middle">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                              <path d="M22 9.24l-7.19-.62L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21L12 17.27L18.18
                               21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27l1-4.28l-3.32-2.88l4.38-.38L12 6.1l1.71
                                4.04l4.38.38l-3.32 2.88l1 4.28L12 15.4z" fill="currentColor"></path>
                            </svg>
                          </n-icon>
                        </template>
                        <span class="icon_font">{{ collectText }}</span>
                      </n-button>
                    </div>
                  </n-space>
                </n-space>
              </div>
            </n-card>
          </div>
          <div class="card_block relative">
            <n-card hoverable title="相关推荐" content-style="padding: 0 8px 8px 8px;" style="height: 100%"
                    header-style="font-size: 1.25rem; padding: 16px 16px 8px 16px" size="medium">
              <div class="card_content">
                <n-layout position="absolute" class="list_content" :native-scrollbar="false">
                  <n-space v-if="showEmptyRelative" justify="center" align="center" class="fill_full">
                    <n-empty description="暂无相关推荐"/>
                  </n-space>
                  <div v-else>
                    <n-list bordered>
                      <n-list-item v-for="(item, index) in dataList" :item="item" :index="index" :key="item.id">
                        <router-link :to="'/post/detail/' + item.id + '?keyword=' + keyword" #="{ navigate, href }"
                                     custom>
                          <n-a tag="div" :underline="false" :href="href" @click="navigate">
                            <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                              <div>
                                {{ spilt_content(item.content) }}
                              </div>
                            </n-space>
                          </n-a>
                        </router-link>
                      </n-list-item>
                    </n-list>
                  </div>
                </n-layout>
              </div>
            </n-card>
          </div>
        </n-space>
      </div>
      <div class="content_row">
        <n-space justify="center" align="center">
          <div class="card_block comments">
            <n-card hoverable title="评论" content-style="padding: 0 8px 8px 8px;" style="height: 100%"
                    header-style="font-size: 1.25rem; padding: 16px 16px 8px 16px" size="medium">
              <div class="card_content">
                <n-layout position="absolute" class="list_content" :native-scrollbar="false">
                  <n-space v-if="showEmpty" justify="center" align="center" class="fill_full">
                    <n-empty description="还没有任何评论"/>
                  </n-space>
                  <div v-else>
                    <n-list bordered>
                      <n-list-item v-for="(item, index) in post_detail.comments" :item="item" :index="index"
                                   :key="item">
                        <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                          <div>
                            {{ index }}
                            <span style="padding-left: 16px"> {{ item }}  </span>
                          </div>
                        </n-space>
                      </n-list-item>
                    </n-list>
                  </div>
                </n-layout>
              </div>
            </n-card>
          </div>
        </n-space>
      </div>
    </n-space>
  </n-layout>
</template>

<script setup>
import {ref, onMounted, inject} from "vue";
import {onBeforeRouteUpdate, useRoute, useRouter} from "vue-router";
import {NLayout, NSpace, NCard, NButton, NIcon, NList, NListItem, NEmpty, NA, useMessage} from "naive-ui";

import BackgroundImage from "@/components/BackgroundImage";

const route = useRoute();
const router = useRouter();
const message = useMessage();

const axios = inject("axios")
const login_status = inject("login")

const post_id = ref(-1)
const dataList = ref([])
const keyword = ref(null)
const post_detail = ref({})
const showEmpty = ref(false)
const showEmptyRelative = ref(false)
const collectText = ref("收藏")
const collectStatus = ref(false)

function spilt_content(content) {
  if (content.length >= 10) {
    return content.substr(0, 10) + "..."
  }
  return content
}

const goBack = () => {
  if (keyword.value == null) {
    // jump to search page
    router.push({path: "/"})
  }
  // jump to search page
  router.push({path: "/search", query: {keyword: keyword.value}})
}

const switchCollectStatus = () => {
  if (!collectStatus.value) {
    axios.post("/api/user/collect/add", {
      Username: login_status.value.username,
      PostId: post_id.value * 1
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      collectStatus.value = true
      collectText.value = "取消"
    })
  } else {
    axios.post("/api/user/collect/remove", {
      Username: login_status.value.username,
      PostId: post_id.value * 1
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      collectStatus.value = false
      collectText.value = "收藏"
    })
  }
}

function queryDetail() {
  axios.post("/api/post/detail", {
    PostId: post_id.value * 1
  }).then(response => {
    if (response.data.status === -1) {
      message.error(response.data.message)
    } else {
      if (response.data.data.result.tags.length === 0) {
        post_detail.value.tags = response.data.data.result.content.substr(0, 4)
      } else {
        post_detail.value.tags = response.data.data.result.tags
      }

      post_detail.value.id = response.data.data.result.id
      post_detail.value.content = response.data.data.result.content
      post_detail.value.username = response.data.data.result.username
      post_detail.value.comments = response.data.data.result.comments
      post_detail.value.reposts_count = response.data.data.result.reposts_count
      post_detail.value.comments_count = response.data.data.result.comments_count
      post_detail.value.attitudes_count = response.data.data.result.attitudes_count
      post_detail.value.time = response.data.data.result.time

      showEmpty.value = post_detail.value.comments.length === 0
    }
  }).then(() => {
    axios.post("/api/search/relative", {
      Keyword: keyword.value, Limit: 5,
      Current: post_id.value * 1
    }).then(response => {
      dataList.value = response.data.data.result
      showEmptyRelative.value = response.data.data.result.length === 0
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  }).then(() => {
    axios.post("/api/user/collect/status", {
      Username: login_status.value.username,
      PostId: post_id.value * 1
    }).then(response => {
      if (response.data.status === -1) {
        console.log(response.data.message)
      }

      if (response.data.status === 0) {
        collectStatus.value = response.data.data.collect
        collectText.value = response.data.data.collect ? "取消" : "收藏"
      }
    })
  }).then(() => {
    axios.post("/api/user/history/add", {
      Username: login_status.value.username,
      PostId: post_id.value * 1
    }).then(response => {
      if (response.data.status === -1) {
        console.log(response.data.message)
      }
    })
  }).catch(err => {
    if (err.response.status === 401) {
      router.push({path: "/login"})
    }
  })
}

onMounted(() => {
  if ("keyword" in route.query) {
    keyword.value = route.query.keyword
  } else {
    console.error("搜索关键词为空")
  }

  if ("id" in route.params) {
    post_id.value = route.params.id
    queryDetail()
  }
})

onBeforeRouteUpdate(to => {
  if ("keyword" in to.query) {
    keyword.value = to.query.keyword
  } else {
    console.error("搜索关键词为空")
  }

  if ("id" in to.params) {
    post_id.value = to.params.id
    queryDetail()
  }
});
</script>

<style scoped>
.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}

.card_block {
  height: 40vh;
  position: relative;
}

.content_row {
  margin-top: 32px;
  width: 100vw;
}

.card_block.detail {
  width: 45vw;
  margin-right: 24px;
}

.card_block.relative {
  width: 15vw;
}

.card_block.comments {
  height: 35vh;
  width: calc(15vw + 45vw + 24px + 12px);
}

.card_content {
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

.icon_font {
  font-size: 20px;
  margin-left: 8px;
  vertical-align: middle
}
</style>

<style>
.n-card-header__extra {
  position: absolute;
}
</style>
