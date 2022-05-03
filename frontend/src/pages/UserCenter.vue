<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-space justify="space-between" align="center" class="full_page">
      <div></div>
      <n-card hoverable header-style="text-align: center; font-size: 1.5rem; padding-bottom: 0;"
              content-style="padding: 8px;" style="background-color: rgba(255, 255, 255, 0.2);">
        <template #header>
          <n-avatar round :size="96" :src="avatar" object-fit="cover" class="item_content"/>
        </template>
        <n-divider style="--n-color: #ECECEC; margin: 12px 0;"></n-divider>
        <div class="user_content">
          <n-space justify="space-between" align="center">
            <div class="left_area">
              <n-h2 prefix="bar" align-text style="margin-bottom: 0">
                个人信息
              </n-h2>
            </div>
            <n-divider vertical style="--n-color: #ECECEC; height: 108px"></n-divider>
            <n-space vertical justify="center" class="right_area">
              <n-space align="center">
                <n-h3 class="item_name">
                  帐号
                </n-h3>
                <n-text class="item_content">
                  {{ username }}
                </n-text>
              </n-space>
              <n-space align="center">
                <n-h3 class="item_name">
                  昵称
                </n-h3>
                <n-text class="item_content">
                  {{ nickname }}
                </n-text>
              </n-space>
              <n-button type="primary" size="small" style="width: 120px" dashed round @click="setModify">
                修改信息
              </n-button>
            </n-space>
          </n-space>
        </div>
        <n-divider style="--n-color: #ECECEC; margin: 12px 0;"></n-divider>
        <div class="user_content">
          <n-space justify="space-between" align="center">
            <div class="left_area">
              <n-h2 prefix="bar" align-text style="margin-bottom: 0">
                浏览记录
              </n-h2>
            </div>
            <n-divider vertical style="--n-color: #ECECEC; height: 108px"></n-divider>
            <n-space vertical justify="center" class="right_area">
              <n-space v-if="show_history_empty" justify="center" align="center" class="fill_full">
                <n-empty description="还没有浏览记录呢" style="--n-icon-color: #3D3D3D; --n-text-color: #3D3D3D"/>
              </n-space>
              <div v-else>
                <n-list bordered style="margin: 0">
                  <n-list-item v-for="(item, index) in history" :item="item" :index="index" :key="item.id"
                               style="padding: 4px 8px">
                    <n-space justify="space-between" align="center" :wrap="false">
                      <div>
                        {{ index + 1 }}
                        <span style="padding-left: 16px">{{ item.content.substr(0, 6) }}...</span>
                      </div>
                      <div>
                        {{ str_time(item.activity_time) }}
                      </div>
                    </n-space>
                  </n-list-item>
                  <n-list-item style="padding: 4px 8px">
                    <n-button type="primary" size="small" style="width: 120px" dashed round @click="goHistory">
                      更多
                    </n-button>
                  </n-list-item>
                </n-list>
              </div>
            </n-space>
          </n-space>
        </div>
        <n-divider style="--n-color: #ECECEC; margin: 12px 0;"></n-divider>
        <div class="user_content">
          <n-space justify="space-between" align="center">
            <div class="left_area">
              <n-h2 prefix="bar" align-text style="margin-bottom: 0">
                我的收藏
              </n-h2>
            </div>
            <n-divider vertical style="--n-color: #ECECEC; height: 108px;"></n-divider>
            <n-space vertical justify="center" class="right_area">
              <n-space v-if="show_collect_empty" justify="center" align="center" class="fill_full">
                <n-empty description="还没有收藏记录呢" style="--n-icon-color: #3D3D3D; --n-text-color: #3D3D3D"/>
              </n-space>
              <div v-else>
                <n-list bordered style="margin: 0">
                  <n-list-item v-for="(item, index) in collect" :item="item" :index="index" :key="item.id"
                               style="padding: 4px 8px">
                    <n-space justify="space-between" align="center" :wrap="false">
                      <div>
                        {{ index + 1 }}
                        <span style="padding-left: 16px">{{ item.content.substr(0, 6) }}...</span>
                      </div>
                      <div>
                        {{ str_time(item.time) }}
                      </div>
                    </n-space>
                  </n-list-item>
                  <n-list-item style="padding: 4px 8px">
                    <n-button type="primary" size="small" style="width: 120px" dashed round @click="goCollect">
                      更多
                    </n-button>
                  </n-list-item>
                </n-list>
              </div>
            </n-space>
          </n-space>
        </div>
        <n-divider style="--n-color: #ECECEC; margin: 12px 0;"></n-divider>
        <div class="user_content">
          <n-space justify="center" align="center">
            <n-a tag="div" :underline="false" href="mailto://209651109@qq.com">联系我们</n-a>
          </n-space>
        </div>
      </n-card>
      <div></div>
    </n-space>
    <n-modal v-model:show="modify" :mask-closable="false" preset="dialog" :show-icon="false" title="修改信息">
      <n-space vertical justify="center">
        <n-space align="center">
          <n-h3 class="item_name">
            帐号
          </n-h3>
          <n-text class="item_content">
            {{ username }}
          </n-text>
        </n-space>
        <n-space align="center">
          <n-h3 class="item_name">
            旧昵称
          </n-h3>
          <n-text class="item_content">
            {{ nickname_old }}
          </n-text>
        </n-space>
        <n-space align="center">
          <n-h3 class="item_name">
            新昵称
          </n-h3>
          <n-input round v-model:value="nickname_new" placeholder="请输入新昵称"/>
        </n-space>
        <n-space align="center">
          <n-h3 class="item_name">
            旧密码
          </n-h3>
          <n-input round v-model:value="password_old" placeholder="请输入旧密码" type="password"/>
        </n-space>
        <n-space align="center">
          <n-h3 class="item_name">
            新密码
          </n-h3>
          <n-input round v-model:value="password_new" placeholder="请输入新密码" type="password"/>
        </n-space>
      </n-space>
      <template #action>
        <n-button type="primary" dashed round @click="updateUserInfo">
          更新信息
        </n-button>
        <n-button type="warning" dashed round @click="setClose" style="margin-left: 8px">
          取消
        </n-button>
      </template>
    </n-modal>
  </n-layout>
</template>

<script setup>
import {ref, onMounted, inject} from "vue";
import {useRoute, useRouter} from "vue-router";
import {
  NLayout, NSpace, NCard, NAvatar, NA,
  NH2, NH3, NList, NListItem, NText, NEmpty,
  NButton, NInput, NModal, NDivider, useMessage
} from "naive-ui";

import BackgroundImage from "@/components/BackgroundImage";

// 是否在修改
const modify = ref(false)

const avatar = ref("")
const username = ref("")
const nickname = ref("")

const nickname_old = ref("")
const nickname_new = ref("")
const password_old = ref("")
const password_new = ref("")

const collect = ref([])
const show_collect_empty = ref(false)

const history = ref([])
const show_history_empty = ref(false)

const route = useRoute();
const router = useRouter();
const message = useMessage();

const md5 = inject("md5")
const axios = inject("axios")
const login_status = inject("login")
const dateFormat = inject("dateFormat")

function str_time(time_str) {
  let date = new Date(time_str)
  return dateFormat("YYYY-mm-dd HH:MM:SS", date)
}

const setClose = () => {
  modify.value = false
}

const setModify = () => {
  nickname_old.value = nickname.value
  nickname_new.value = nickname.value
  modify.value = true
}

const goHistory = () => {
  router.push({path: "/user/" + login_status.value.username + "/history"})
}

const goCollect = () => {
  router.push({path: "/user/" + login_status.value.username + "/collect"})
}

const updateUserInfo = () => {
  let md5_password_old = md5(password_old.value)
  let md5_password_new = md5(password_new.value)

  axios.post("/api/user/info/update", {
    Username: login_status.value.username,
    Nickname: nickname_new.value,
    PasswordOld: md5_password_old,
    PasswordNew: md5_password_new,
  }).then(response => {
    if (response.data.status === -1) {
      message.error(response.data.message)
      return
    }

    avatar.value = response.data.data.avatar
    username.value = response.data.data.username
    nickname.value = response.data.data.nickname

    password_old.value = ""
    password_new.value = ""

    message.success("更新成功")
  }).catch(() => {
    message.error("网络错误");
  }).finally(() => {
    setClose()
  })
}

onMounted(() => {
  let username_local = ""
  if ("username" in route.params) {
    username_local = route.params.username

    axios.post("/api/user/info", {
      Username: username_local,
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      avatar.value = response.data.data.avatar
      username.value = response.data.data.username
      nickname.value = response.data.data.nickname
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
      message.error("网络错误");
    })

    axios.post("/api/user/history/all", {
      Username: username_local,
      Limit: 5
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      history.value = response.data.data.result
      show_history_empty.value = response.data.data.result.length === 0
    })

    axios.post("/api/user/collect/all", {
      Username: username_local,
      Limit: 5
    }).then(response => {
      if (response.data.status === -1) {
        message.error(response.data.message)
      }

      collect.value = response.data.data.result
      show_collect_empty.value = response.data.data.result.length === 0
    })
  }
})
</script>

<style scoped>
.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}

.user_content {
  padding: 0 8px;
  width: 720px;
  text-align: center;
  position: relative;
}

.left_area {
  margin-left: 32px;
}

.right_area {
  margin-right: 32px;
}

.item_name {
  width: 80px;
  text-align: right;
  margin-bottom: 0;
}

.user_content .left_area {
  width: 100%;
}

.user_content .right_area {
  min-width: 480px;
}

.user_content .item_name {
  padding: 8px;
  width: 120px;
  text-align: right;
}

.user_content .item_name::after {
  content: "：";
}

.user_content .item_content {
  margin-left: 8px;
  font-size: 1.5rem;
}

</style>