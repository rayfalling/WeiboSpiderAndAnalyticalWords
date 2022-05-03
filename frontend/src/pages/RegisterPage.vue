<template>
  <n-layout class="full_page">
    <BackgroundImage />
    <n-space justify="space-between" align="center" class="full_page">
      <div></div>
      <n-config-provider :theme-overrides="themeOverrides">
        <n-card hoverable title="注&nbsp;&nbsp;&nbsp;&nbsp;册"
                header-style="text-align: center; font-size: 1.5rem" content-style="padding: 8px;"
                style="background-color: rgba(255, 255, 255, 0.2);">
          <div class="card_content">
            <n-form ref="formRef" :model="model" label-placement="left" :show-require-mark="false"
                    :label-width="label_width" :rules="rules">
              <n-form-item label="账&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号" path="username">
                <n-input round v-model:value="model.username" placeholder="请输入手机"/>
              </n-form-item>
              <n-form-item label="昵&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;称" path="nickname">
                <n-input round v-model:value="model.nickname" placeholder="请输入用户名"/>
              </n-form-item>
              <n-form-item label="密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码" path="password">
                <n-input round v-model:value="model.password" placeholder="仅限数字或字母或组合" type="password"
                         @input="handlePasswordInput" @keydown.enter.prevent/>
              </n-form-item>
              <n-form-item ref="reenterPassword" label="确认密码" path="reenteredPassword" first>
                <n-input round v-model:value="model.reenteredPassword" placeholder="请再次输入密码"
                         :disabled="!model.password" type="password" @keydown.enter.prevent/>
              </n-form-item>
            </n-form>
          </div>
          <n-space vertical align="center" style="padding-bottom: 16px">
            <n-button circle style="padding: 8px 128px" type="primary" size="large" @click="onRegister">
              注&nbsp;&nbsp;&nbsp;&nbsp;册
            </n-button>
            <n-button text type="info" @click="onLoginClick">
              已有账号？
            </n-button>
          </n-space>
        </n-card>
      </n-config-provider>
      <div></div>
    </n-space>
  </n-layout>
</template>

<script setup>
import {ref, inject} from "vue";
import {useRouter} from 'vue-router'
import {NLayout, NCard, NSpace, NForm, NFormItem, NInput, NButton, NConfigProvider, useMessage} from "naive-ui";

import BackgroundImage from "@/components/BackgroundImage";

const label_width = 64;
const formRef = ref(null);
const reenterPassword = ref(null);

const model = ref({
  username: "",
  nickname: "",
  password: "",
  reenteredPassword: ""
});

function validatePasswordStartWith(rule, value) {
  return !!model.value.password && model.value.password.startsWith(value) && model.value.password.length >= value.length;
}

function validatePasswordSame(rule, value) {
  return value === model.value.password;
}

function validatePhoneNumber(rule, value) {
  return value.length === 11;
}

function handlePasswordInput() {
  if (model.value.reenteredPassword) {
    reenterPassword.value?.validate({trigger: "password-input"});
  }
}

const rules = {
  username: [
    {
      required: true,
      message: "请输入账号"
    }, {
      validator: validatePhoneNumber,
      required: true,
      message: "手机号长度为11位"
    }
  ],
  nickname: [
    {
      required: true,
      message: "请输入昵称"
    }
  ],
  password: [
    {
      required: true,
      message: "请输入密码"
    }
  ],
  reenteredPassword: [
    {
      required: true,
      message: "请再次输入密码",
      trigger: ["input", "blur"]
    }, {
      validator: validatePasswordStartWith,
      message: "两次密码输入不一致",
      trigger: "input"
    }, {
      validator: validatePasswordSame,
      message: "两次密码输入不一致",
      trigger: ["blur", "password-input"]
    }
  ]
};

const themeOverrides = {
  NCard: {
    nColor: "rgba(255, 255, 255, 0.4)"
  },
}

const router = useRouter();
const message = useMessage();

const md5 = inject("md5")
const axios = inject("axios")

const onLoginClick = () => {
  router.push({path: "/login"})
}

const onRegister = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      let md5_password = md5(model.value.password)

      axios.post("/api/register", {
            Username: model.value.username,
            Nickname: model.value.nickname,
            Password: md5_password
          }
      ).then(response => {
        if (response.data.status === 0) {
          message.info(response.data.message)
          onLoginClick();
        } else {
          message.error(response.data.message)
        }
      }).catch(() => {
        message.error("网络错误");
      })
    } else {
      message.error("注册失败");
    }
  })
}

</script>

<style scoped>
.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}

.card_content {
  padding: 16px 8px 16px 8px;
  width: 360px;
  text-align: center;
}
</style>
