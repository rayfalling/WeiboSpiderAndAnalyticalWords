# coding: utf-8

# 抓取数据模板地址
# 基于 m.weibo.cn 抓取数据，无需登陆验证
# noinspection SpellCheckingInspection
search_url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={" \
                      "}&containerid=100103type=61%26q%3D{}&page={} "

# 微博详情获取
content_url_template = "https://m.weibo.cn/statuses/extend?id={}"

# 详情页面数据(不需要登录态), 限制每次只能获取3页数据
comment_url_template = "https://m.weibo.cn/api/comments/show?id={}&page={}"

# 全部评论信息(不需要登录态), 限制每次只能获取1页数据
hot_flow_url_template = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0"

# 全部评论信息(需要登录态)
hot_flow_login_url_template = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=1"

# 是否使用代理
use_request_proxy = True

# 请求代理
request_proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# request headers
# 未来获取所有评论信息需要 Cookie
headers = {
    "Host": "m.weibo.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/99.0.4844.84 Safari/537.36",
    "Cookie": ""  # 这里将浏览器的cookie复制过来进行了。
}

# 多进程并发进程数
multi_processing_pool_core_count = 4

# 无效内容关键词
invalid_keyword = {
    "的微博视频": False,
    "微博问答": True
}
