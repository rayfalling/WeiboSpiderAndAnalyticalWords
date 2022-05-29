<template>
  <div class="background-image-container">
    <img :src="require('@/assets/bg1.jpg')" alt=""/>
  </div>
</template>

<script>
export default {
  name: 'BackgroundImage'
}
</script>

<style scoped>
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