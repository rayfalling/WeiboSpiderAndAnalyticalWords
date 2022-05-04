<!--suppress JSUnresolvedFunction -->
<template>
  <n-layout embedded class="full_page">
    <BackgroundImage/>
    <n-space vertical align="center" justify="center" style="position: relative">
      <div class="content_row">
        <n-space justify="center" align="center">
          <SearchInput width="640px" placeholder="请输入关键词" @on-search-clicked="onSearch" :content="keyword"/>
        </n-space>
      </div>
      <div class="content_row">
        <n-space justify="center" align="center">
          <div class="card_block detail">
            <n-card hoverable content-style="padding: 0 8px 8px 8px;" style="height: 100%" size="medium">
              <template #header>
                <n-space align="center">
                  <n-h2 prefix="bar" align-text style="margin-bottom: 0">
                    <n-text type="primary">词云热榜</n-text>
                  </n-h2>
                </n-space>
              </template>
              <div id="word_cloud" class="card_content"></div>
            </n-card>
          </div>
          <div class="card_block right_area">
            <n-card hoverable content-style="padding: 0 8px 8px 8px;" style="height: 100%" size="medium"
                    header-style="padding: 16px 16px 8px 16px">
              <template #header>
                <n-space justify="space-around">
                  <div>
                    <n-space align="center">
                      <n-h2 align-text style="margin-bottom: 0">
                        <n-text type="primary">热度上升</n-text>
                      </n-h2>
                    </n-space>
                  </div>
                  <div>
                    <n-space align="center">
                      <n-h2 align-text style="margin-bottom: 0">
                        <n-text type="primary">热度下降</n-text>
                      </n-h2>
                    </n-space>
                  </div>
                </n-space>
              </template>
              <div class="card_content">
                <n-layout position="absolute" class="list_content" :native-scrollbar="false">
                  <n-space justify="space-around" class="fill_full">
                    <n-space v-if="showEmptyIncrease" justify="center" align="center" class="card_item">
                      <n-empty description="暂无热度上升数据"/>
                    </n-space>
                    <div v-else class="card_item">
                      <n-list bordered>
                        <n-list-item v-for="(item, index) in increaseList" style="padding: 12px 0"
                                     :item="item" :index="index" :key="item.key">
                          <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                            <div>
                              {{ index + 1 }}
                              <span style="padding-left: 8px"> {{ item.key }}  </span>
                            </div>
                          </n-space>
                        </n-list-item>
                      </n-list>
                    </div>

                    <n-space v-if="showEmptyDecrease" justify="center" align="center" class="card_item">
                      <n-empty description="暂无热度下降数据"/>
                    </n-space>
                    <div v-else class="card_item">
                      <n-list bordered>
                        <n-list-item v-for="(item, index) in decreaseList" style="padding: 12px 0"
                                     :item="item" :index="index" :key="item.key">
                          <n-space justify="space-between" align="center" item-style="padding: 16px" :wrap="false">
                            <div>
                              {{ index + 1 }}
                              <span style="padding-left: 8px"> {{ item.key }}  </span>
                            </div>
                          </n-space>
                        </n-list-item>
                      </n-list>
                    </div>
                  </n-space>
                </n-layout>
              </div>
            </n-card>
          </div>
        </n-space>
      </div>
      <div class="content_row">
        <n-space justify="center" align="center">
          <div class="card_block comments">
            <n-card hoverable content-style="padding: 0 8px 8px 8px;" style="height: 100%" size="medium">
              <template #header>
                <n-space align="center">
                  <n-h2 prefix="bar" align-text style="margin-bottom: 0">
                    <n-text type="primary">热度趋势</n-text>
                  </n-h2>
                </n-space>
              </template>
              <div id="trend" class="card_content"></div>
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
import {NLayout, NSpace, NCard, NH2, NText, NList, NListItem, NEmpty} from "naive-ui";

import SearchInput from "@/components/SearchInput";
import BackgroundImage from "@/components/BackgroundImage";

require("echarts-wordcloud");

const route = useRoute();
const router = useRouter();

const axios = inject("axios")
const echarts = inject("echarts")
// const isAdmin = inject("isAdmin")
const dateFormat = inject("dateFormat")

const keyword = ref(null)
const wordCloudList = ref([])

const trendList = ref([])
const trendListPredict = ref([])

const decreaseList = ref([])
const increaseList = ref([])
const showEmptyDecrease = ref(false)
const showEmptyIncrease = ref(false)

const neutral_color = ref("#000000")
const negative_color = ref("#000000")
const positive_color = ref("#000000")

let trend = null
let word_cloud = null

function str_time(time_str) {
  let date = new Date(time_str)
  return dateFormat("mm-dd HH:00", date)
}

const onSearch = (word) => {
  console.log(word)
  router.push({path: "/latest", query: {keyword: word}})
}

function map_emotion_to_color(emotion) {
  if (emotion === 0) {
    return neutral_color.value
  } else if (emotion === -1) {
    return negative_color.value
  } else if (emotion === 1) {
    return positive_color.value
  } else {
    return "#000000"
  }
}

function showWordCloud() {
  if (word_cloud != null) {
    word_cloud.dispose()
  }

  word_cloud = echarts.init(document.getElementById("word_cloud"));

  let data_list = []
  wordCloudList.value.forEach((item, index) => {
    data_list[index] = {
      name: item.key,
      value: item.count,
      textStyle: {
        color: map_emotion_to_color(item.emotion)
      }
    }
  })

  word_cloud.setOption({
    series: [
      {
        type: "wordCloud",
        keepAspect: false,
        left: "center",
        top: "center",
        right: null,
        bottom: null,
        sizeRange: [24, 60],
        rotationRange: [0, 0],
        data: data_list
      }
    ]
  });
}

function showTrendArea() {
  if (trend != null) {
    trend.dispose()
  }

  trend = echarts.init(document.getElementById("trend"));

  let x_axis = []
  let trend_data = []
  let trend_data_predict = []

  trendList.value.forEach((item, index) => {
    x_axis[index] = str_time(item["time_point"])
    trend_data[index] = [str_time(item["time_point"]), item["trend"]]
    trend_data_predict[index] = [str_time(item["time_point"]), item["trend"]]
  })

  trendListPredict.value.forEach((item, index) => {
    x_axis[trendList.value.length + index] = str_time(item["time_point"])
    trend_data[trendList.value.length + index] = [str_time(item["time_point"]), "-"]
    trend_data_predict[trendList.value.length + index] = [str_time(item["time_point"]), item["trend"]]
  })

  let linear_color = {
    type: 'linear',
    x: 0,
    y: 0,
    x2: 0,
    y2: 2,
    colorStops: [{
      offset: 0,
      color: "rgba(239, 137, 27, 0.3)"
    }, {
      offset: 1,
      color: "rgba(239, 137, 27, 0.8)"
    }],
  }

  trend.setOption({
    legend: {
      orient: "vertical",
      x: "right",
      y: "center",
      data: [
        {
          name: "实时热度",
          icon: "rect",
          itemStyle: {
            color: linear_color
          }
        },
        {
          name: "预测热度",
          icon: "rect",
          itemStyle: {
            color: "rgb(89, 170, 140)"
          }
        },
      ]
    },
    xAxis: [
      {
        type: "category",
        boundaryGap: false,
        data: x_axis
      }
    ],
    yAxis: [{type: "value"}],
    series: [
      {
        name: "实时热度",
        type: "line",
        smooth: true,
        showSymbol: false,
        label: {
          show: true,
          formatter: '{b}'
        },
        lineStyle: {
          width: 0,
        },
        areaStyle: {
          opacity: 0.8,
          color: linear_color
        },
        emphasis: {
          focus: "series"
        },
        data: trend_data
      },
      {
        name: "预测热度",
        type: "line",
        smooth: true,
        showSymbol: false,
        lineStyle: {
          color: "rgb(89, 170, 140)",
          type: "dashed",
          join: "round"
        },
        emphasis: {
          focus: "series"
        },
        data: trend_data_predict
      },
    ]
  });
}

function querySearch() {
  if (keyword.value === "") {
    axios.post("/api/word_cloud/all").then(response => {
      if ("word_cloud" in response.data.data) {
        wordCloudList.value = response.data.data["word_cloud"]
      }

      if ("config" in response.data.data) {
        neutral_color.value = response.data.data.config.color[0]
        positive_color.value = response.data.data.config.color[1]
        negative_color.value = response.data.data.config.color[-1]
      }

      showWordCloud()
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  } else {
    axios.post("/api/word_cloud/search", {
      Keyword: keyword.value
    }).then(response => {
      if ("word_cloud" in response.data.data) {
        wordCloudList.value = response.data.data["word_cloud"]
      }

      if ("config" in response.data.data) {
        neutral_color.value = response.data.data.config.color[0]
        positive_color.value = response.data.data.config.color[1]
        negative_color.value = response.data.data.config.color[-1]
      }

      showWordCloud()
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  }
}

function queryTrend() {
  if (keyword.value === "") {
    axios.post("/api/word_trend/all").then(response => {
      if ("word_trend" in response.data.data) {
        decreaseList.value = response.data.data["word_trend"]["decrease"]
        increaseList.value = response.data.data["word_trend"]["increase"]

        showEmptyDecrease.value = response.data.data["word_trend"]["decrease"].length === 0
        showEmptyIncrease.value = response.data.data["word_trend"]["increase"].length === 0
      }
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  } else {
    axios.post("/api/word_trend/search", {
      Keyword: keyword.value
    }).then(response => {
      if ("word_trend" in response.data.data) {
        decreaseList.value = response.data.data["word_trend"]["decrease"]
        increaseList.value = response.data.data["word_trend"]["increase"]

        showEmptyDecrease.value = response.data.data["word_trend"]["decrease"].length === 0
        showEmptyIncrease.value = response.data.data["word_trend"]["increase"].length === 0
      }
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  }
}

function queryHotTrend() {
  if (keyword.value === "") {
    axios.post("/api/word_hot_trend/all").then(response => {
      if ("word_hot_trend" in response.data.data && "word_hot_trend_predict" in response.data.data) {
        trendList.value = response.data.data["word_hot_trend"]
        trendListPredict.value = response.data.data["word_hot_trend_predict"]
      }

      showTrendArea()
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  } else {
    axios.post("/api/word_hot_trend/search", {
      Keyword: keyword.value
    }).then(response => {
      if ("word_hot_trend" in response.data.data && "word_hot_trend_predict" in response.data.data) {
        trendList.value = response.data.data["word_hot_trend"]
        trendListPredict.value = response.data.data["word_hot_trend_predict"]
      }

      showTrendArea()
    }).catch(err => {
      if (err.response.status === 401) {
        router.push({path: "/login"})
      }
    })
  }
}

onMounted(() => {
  if ("keyword" in route.query) {
    keyword.value = route.query.keyword
  } else {
    keyword.value = ""
  }

  queryTrend()
  querySearch()
  queryHotTrend()
})

onBeforeRouteUpdate(to => {
  if ("keyword" in to.query) {
    keyword.value = to.query.keyword
  } else {
    keyword.value = ""
  }

  queryTrend()
  querySearch()
  queryHotTrend()
});
</script>

<style scoped>
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

.card_block {
  height: 35vh;
  position: relative;
}

.content_row {
  margin-top: 32px;
  width: 100vw;
}

.card_block.detail {
  width: 35vw;
  margin-right: 24px;
}

.card_block.right_area {
  width: 25vw;
}

.card_item {
  width: calc((25vw - 60px) / 2);
  height: 100%;
}

.card_block.comments {
  height: 35vh;
  width: calc(15vw + 45vw + 24px + 12px);
}

.card_content {
  height: 100%;
  position: relative;
}
</style>