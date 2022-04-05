# coding: utf-8

import re
import json
import requests

from libs.logger import FormatLogger
from config.spider_config import search_url_template, use_request_proxy, request_proxies


def clean_text(text):
    """清除文本中的标签等信息"""
    dr = re.compile(r"(<)[^>]+>", re.S)
    dd = dr.sub("", text)
    dr = re.compile(r"#[^#]+#", re.S)
    dd = dr.sub("", dd)
    dr = re.compile(r"@[^ ]+ ", re.S)
    dd = dr.sub("", dd)
    return dd.strip()


def fetch_data(query_val, page_id):
    """抓取关键词某一页的数据"""
    if use_request_proxy:
        resp = requests.get(search_url_template.format(query_val, query_val, page_id), proxies=request_proxies)
    else:
        resp = requests.get(search_url_template.format(query_val, query_val, page_id))

    card_group = json.loads(resp.text)["data"]["cards"][0]["card_group"]
    FormatLogger.debug("[Spider]", "url：{}  --- 条数: {}".format(resp.url, len(card_group)))

    m_blogs = []  # 保存处理过的微博
    for card in card_group:
        mblog = card["mblog"]
        FormatLogger.debug("[Spider]", json.dumps(card, ensure_ascii=False, indent=4))
        blog = {
            "mid": mblog["id"],  # 微博id
            "time": clean_text(mblog["created_at"]),  # 时间
            "text": clean_text(mblog["text"]),  # 文本
            "userid": str(mblog["user"]["id"]),  # 用户id
            "username": mblog["user"]["screen_name"],  # 用户名
            "reposts_count": mblog["reposts_count"],  # 转发
            "comments_count": mblog["comments_count"],  # 评论
            "attitudes_count": mblog["attitudes_count"]  # 点赞
        }
        m_blogs.append(blog)
    return m_blogs


def remove_duplication(m_blogs):
    """根据微博的id对微博进行去重"""
    mid_set = {m_blogs[0]["mid"]}
    new_blogs = []
    for blog in m_blogs[1:]:
        if blog["mid"] not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog["mid"])
    return new_blogs


def fetch_pages(query_val, page_num):
    """抓取关键词多页的数据"""
    mblogs = []
    for page_id in range(1 + page_num + 1):
        try:
            mblogs.extend(fetch_data(query_val, page_id))
        except Exception as e:
            print(e)

    print("去重前：", len(mblogs))
    mblogs = remove_duplication(mblogs)
    print("去重后：", len(mblogs))

    # 保存到 result.json 文件中
    fp = open("result_{}.json".format(query_val), "w", encoding="utf-8")
    json.dump(mblogs, fp, ensure_ascii=False, indent=4)
    print("已保存至 result_{}.json".format(query_val))
