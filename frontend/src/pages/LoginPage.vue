<template>
  <n-layout embedded class="full_page">
    <div class="background-image-container">
      <img :src="require('@/assets/bg.jpg')" alt=""/>
    </div>
    <n-space justify="space-between" align="center" class="full_page">
      <div></div>
      <n-card bordered embedded hoverable title="登&nbsp;&nbsp;&nbsp;&nbsp;录"
              header-style="text-align: center; font-size: 1.5rem" content-style="padding: 8px;" size="large"
              style="background-color: rgba(255, 255, 255, 0.2);">
        <div class="card_content">
          <n-form ref="formRef" :model="model" label-placement="left" :label-width="label_width">
            <n-form-item label="账号" path="username">
              <n-input round v-model:value="model.username" placeholder="请输入账号"/>
            </n-form-item>
            <n-form-item label="密码" path="password">
              <n-input round v-model:value="model.password" placeholder="请输入密码"
                       type="password" @keydown.enter.prevent/>
            </n-form-item>
          </n-form>
        </div>
        <n-space vertical align="center" style="padding-bottom: 16px">
          <n-button circle style="padding: 8px 128px" type="primary" size="large">
            登&nbsp;&nbsp;&nbsp;&nbsp;录
          </n-button>
          <n-button text type="info" @click="onRegisterClicked">
            还没有账号？
          </n-button>
        </n-space>
      </n-card>
      <div></div>
    </n-space>
  </n-layout>
</template>

<script setup>
import {ref} from "vue";
import {useRouter} from 'vue-router'
import {NLayout, NCard, NSpace, NForm, NFormItem, NInput, NButton} from "naive-ui";

const label_width = 64;
const formRef = ref(null);

const model = ref({
  username: "",
  password: ""
});

const router = useRouter()

const onRegisterClicked = () => {
  router.push({path: "/register"})
}

</script>

<style scoped>
.full_page {
  width: 100%;
  height: 100%;
  position: relative;
}

.card_content {
  padding: 16px 8px;
  width: 360px;
  text-align: center;
}

.background-image-container {
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  position: absolute;
}

.background-image-container img {
  width: 100vw;
  height: 100vh;
}
</style>