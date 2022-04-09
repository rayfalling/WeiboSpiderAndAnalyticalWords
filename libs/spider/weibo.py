# coding: utf-8
import json
import multiprocessing
import os.path
import typing
from time import sleep
from typing import Tuple, Any

import requests
import requests.utils

from datetime import datetime

from requests import Response

from libs.logger import FormatLogger
from libs.helper import clean_text, get_temp_dir
from libs.data_model.weibo_data_fetch import PostData, PostDataEncoder
from config.spider_config import content_url_template, multi_processing_pool_core_count, invalid_keyword
from config.spider_config import search_url_template, use_request_proxy, request_proxies, comment_url_template


def fetch_data(url: str) -> tuple[Any, Response]:
    if use_request_proxy:
        response = requests.get(url, proxies=request_proxies)
    else:
        response = requests.get(url)

    return json.loads(response.text), response


def fetch_post(query_val: str, page_id: int) -> typing.List[typing.Union[typing.Any, PostData]]:
    """
    获取关键词实时微博数据

    :param query_val: 搜索关键词
    :param page_id: 获取分页页数
    :return:
    """
    json_response, response = fetch_data(search_url_template.format(query_val, query_val, page_id))
    card_group = json_response["data"]["cards"]
    FormatLogger.info("Spider", "抓取Url：{} 条数: {}".format(requests.utils.unquote(response.url), len(card_group)))

    # 当前处理微博数据
    m_blogs = []
    for card in card_group:
        mblog = card["mblog"]

        # 转换返回的时间
        create_time = mblog["created_at"]
        post_time = datetime.strptime(create_time, "%a %b %d %H:%M:%S %z %Y")

        simple_content, tags, links = clean_text(mblog["text"])
        simple_content = simple_content.strip()
        tags = [tag.replace("#", "") for tag in tags]

        next_card = False
        for keyword, force_skip in invalid_keyword.items():
            for text in links:
                if keyword in text and (simple_content.strip() == "" or force_skip):
                    next_card = True

        if next_card:
            continue

        # 建立对象
        blog = PostData(
            mid=int(mblog["id"]), user_id=mblog["user"]["id"], username=mblog["user"]["screen_name"], tags=tags,
            content=simple_content, post_time=post_time, attitudes_count=mblog["attitudes_count"],
            comments_count=mblog["comments_count"], reposts_count=mblog["reposts_count"]
        )

        blog.set_scheme(card["scheme"])
        m_blogs.append(blog)

    return m_blogs


def fetch_content_and_commit(blog: PostData) -> PostData:
    """
    获取微博正文内容和评论数据

    :param blog: 微博内容
    :return:
    """

    if "全文" in blog.content:
        json_response, _ = fetch_data(content_url_template.format(blog.mid))
        if "ok" in json_response and "data" in json_response:
            content, _, _ = clean_text(json_response["data"]["longTextContent"])
            blog.set_content(content=content)

    if blog.comment.count > 0:
        # TODO 获取微博登录态爬取评论
        # Try fetch one-page comment
        for page in range(2):
            json_response, response = fetch_data(comment_url_template.format(blog.mid, page))
            # 301 重定向时数据为空
            if response.status_code == 301:
                break

            # 当前页暂无数据
            if "ok" in json_response and json_response.get("ok") == 0:
                break

            comment_data = json_response["data"]["data"]
            for comment in comment_data:
                if comment["id"] in blog.comment.comment:
                    continue

                content, _, _ = clean_text(comment["text"])
                if content == "":
                    continue

                blog.comment.comment[comment["id"]] = content

    return blog


def remove_duplication(m_blogs: typing.List[PostData]) -> typing.List[typing.Union[typing.Any, PostData]]:
    """
    根据微博的id对微博进行去重
    """
    new_blogs = [m_blogs[0]]
    mid_set: typing.Set[int] = {m_blogs[0].mid}

    for blog in m_blogs[1:]:
        if blog.mid not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog.mid)

    return new_blogs


def fetch_pages(query_val, page_num) -> typing.List[typing.Union[typing.Any, PostData]]:
    """抓取关键词多页的数据"""
    blogs: typing.List[typing.Union[typing.Any, PostData]] = []
    for page_id in range(page_num):
        try:
            blogs.extend(fetch_post(query_val, page_id))
            # 强制线程睡眠, 减少撞上微博限制频次
            sleep(0.01)
        except Exception as error:
            FormatLogger.info("Spider", str(error))

    # 数据去重
    before_count = len(blogs)
    if before_count == 0:
        return []

    blogs = remove_duplication(blogs)
    FormatLogger.info("Spider", "去重前: {} 去重后: {}".format(before_count, len(blogs)))

    # 强制线程睡眠, 减少撞上微博限制频次
    sleep(0.01)

    FormatLogger.info("Spider", "Fetch full content and commit per post...")
    with multiprocessing.Pool(multi_processing_pool_core_count) as pool:
        blogs = pool.map(fetch_content_and_commit, blogs)
        pool.close()
        pool.join()
    FormatLogger.info("Spider", "Fetch full content and commit per post success")

    # 保存到 result.json 文件中
    file_name = "result_{}_{}.json".format(query_val, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    file_path = os.path.abspath(os.path.join(get_temp_dir(), "spider_result", file_name))
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(blogs, fp, ensure_ascii=False, indent=4, cls=PostDataEncoder)
        FormatLogger.info("Spider", "本次抓取结果已保存至 {}".format(file_path))

    return blogs
