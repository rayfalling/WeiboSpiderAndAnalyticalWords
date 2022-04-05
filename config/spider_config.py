# coding: utf-8

# 抓取数据模板地址
# 基于 m.weibo.cn 抓取数据，无需登陆验证
# noinspection SpellCheckingInspection
search_url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{" \
                      "}&page={} "

# 详情页面数据
status_url_template = "https://m.weibo.cn/statuses/show?id={}"

# 是否使用代理
use_request_proxy = True

# 请求代理
request_proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 无效内容关键词
invalid_keyword = ["的微博视频", ]

# 固定搜索的关键词
search_keyword = ["鸿星尔克", ]
