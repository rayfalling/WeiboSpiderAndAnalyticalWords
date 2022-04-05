# coding: utf-8
import json
import multiprocessing
import os.path
import typing

import requests
import requests.utils

from datetime import datetime

from libs.logger import FormatLogger
from libs.helper import clean_text, get_temp_dir
from libs.data_model.weibo_data_fetch import PostData, PostDataEncoder
from config.spider_config import search_url_template, use_request_proxy, request_proxies, status_url_template
from config.spider_config import content_url_template, multi_processing_pool_core_count


def fetch_post(query_val: str, page_id: int):
    """
    获取关键词实时微博数据

    :param query_val: 搜索关键词
    :param page_id: 获取分页页数
    :return:
    """
    if use_request_proxy:
        response = requests.get(search_url_template.format(query_val, query_val, page_id), proxies=request_proxies)
    else:
        response = requests.get(search_url_template.format(query_val, query_val, page_id))

    json_response = json.loads(response.text)
    card_group = json_response["data"]["cards"]
    FormatLogger.info("Spider", "抓取Url：{} 条数: {}".format(requests.utils.unquote(response.url), len(card_group)))

    # 当前处理微博数据
    m_blogs = []
    for card in card_group:
        mblog = card["mblog"]

        # 转换返回的时间
        create_time = mblog["created_at"]
        post_time = datetime.strptime(create_time, "%a %b %d %H:%M:%S %z %Y")

        # 建立对象
        blog = PostData(
            mid=int(mblog["id"]), user_id=mblog["user"]["id"], username=mblog["user"]["screen_name"],
            content=clean_text(mblog["text"]), post_time=post_time, attitudes_count=mblog["attitudes_count"],
            comments_count=mblog["comments_count"], reposts_count=mblog["reposts_count"]
        )

        blog.set_scheme(card["scheme"])
        m_blogs.append(blog)

    return m_blogs


def fetch_content_and_commit(blog: PostData):
    """
    获取微博正文内容和评论数据

    :param blog: 微博内容
    :return:
    """

    if "全文" in blog.content:
        if use_request_proxy:
            response = requests.get(content_url_template.format(blog.mid), proxies=request_proxies)
        else:
            response = requests.get(status_url_template.format(blog.mid))

        json_response = json.loads(response.text)
        if "ok" in json_response and "data" in json_response:
            blog.set_content(clean_text(json_response["data"]["longTextContent"]))

    # TODO 获取评论数据

    return blog


def remove_duplication(m_blogs: typing.List[PostData]):
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


def fetch_pages(query_val, page_num):
    """抓取关键词多页的数据"""
    blogs: typing.List[typing.Union[typing.Any, PostData]] = []
    for page_id in range(page_num):
        try:
            blogs.extend(fetch_post(query_val, page_id))
        except Exception as error:
            FormatLogger.info("Spider", str(error))

    # 数据去重
    before_count = len(blogs)
    blogs = remove_duplication(blogs)
    FormatLogger.info("Spider", "去重前: {} 去重后: {}".format(before_count, len(blogs)))

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
