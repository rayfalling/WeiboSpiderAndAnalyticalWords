<template>
  <div :style="{'width': width}">
    <n-input size="large" round :placeholder="placeholder" v-model:value="searchContent" @keyup="onKeyUp">
      <template #prefix>
        <n-icon size="32">
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 512 512" xml:space="preserve">
                <g><g><g><g>
                  <path d="M337.509,305.372h-17.501l-6.571-5.486c20.791-25.232,33.922-57.054,33.922-93.257
					C347.358,127.632,283.896,64,205.135,64C127.452,64,64,127.632,64,206.629s63.452,142.628,142.225,142.628
					c35.011,0,67.831-13.167,92.991-34.008l6.561,5.487v17.551L415.18,448L448,415.086L337.509,305.372z M206.225,305.372
					c-54.702,0-98.463-43.887-98.463-98.743c0-54.858,43.761-98.742,98.463-98.742c54.7,0,98.462,43.884,98.462,98.742
					C304.687,261.485,260.925,305.372,206.225,305.372z"></path>
                </g></g></g></g>
              </svg>
        </n-icon>
      </template>
      <template #suffix>
        <n-divider vertical/>
        <n-button ghost text @click="onSearchClicked">
          搜索
        </n-button>
      </template>
    </n-input>
  </div>
</template>

<script>
import {ref, toRefs} from "vue";
import {NDivider, NInput, NButton, NIcon} from "naive-ui";

export default {
  setup(props, context) {
    let searchContent = ref(null)

    const onKeyUp = keyboardEvent => {
      if (keyboardEvent.keyCode === 13 && !keyboardEvent.ctrlKey && !keyboardEvent.altKey && !keyboardEvent.shiftKey) {
        context.emit("on-search-clicked", searchContent.value)
      }
    }

    const onSearchClicked = () => {
      context.emit("on-search-clicked", searchContent.value)
    }

    return {
      ...toRefs(props),

      onKeyUp,
      onSearchClicked,
      searchContent
    }
  },
  name: "SearchInput",
  components: {
    NButton, NInput, NIcon, NDivider
  },
  props: {
    placeholder: {
      type: String,
      default() {
        return "请输入搜索内容"
      }
    } ,
    width: {
      type: String,
      default() {
        return "480px"
      }
    }
  }
}
</script>

<style scoped>
.background-image-container img {
  width: 100vw;
  height: 100vh;
}
</style>