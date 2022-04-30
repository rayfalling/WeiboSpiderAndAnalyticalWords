import json

from flask import Blueprint, request, jsonify

from libs import fetch_pages, FormatLogger, word_split
from libs.data_model import PostData, PostDataContent, WordFrequency

from config.flask_config import MULTI_PROCESS_JIEBA

from .common import process_after_request

from ..thread_pool import submit_function_async, parallel_function_with_waiting_result
from ..functions import insert_all_post_data, insert_all_word_split_data, query_all_post_and_comment_by_keyword

admin_router = Blueprint("admin", __name__)
admin_router.after_request(process_after_request)

__all__ = ("admin_router",)


@admin_router.route("/admin/spider/update", methods=["POST"])
def request_spider_update():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_pages = request_json.get("Pages", 0)
    request_keyword = request_json.get("Keyword", "")

    if request_pages == 0 or request_keyword == "":
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    try:
        result = fetch_pages(request_keyword, request_pages)
    except (RuntimeError, ValueError, IndexError):
        FormatLogger.error("AdminRouter", "Spider returns error")
        response_data["message"] = "数据抓取错误"
        return jsonify(response_data)

    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"] = {
        "spider_count": len(result)
    }

    # 异步线程开始处理分词结果
    submit_function_async(spider_update_database, result)

    return jsonify(response_data)


def spider_update_database(post_list: list[PostData]):
    """
    提交并更新数据库，完成分词操作

    :param post_list:
    :return:
    """
    if len(post_list) == 0:
        return

    FormatLogger.info("Database", "Writing all spider data to database......")
    insert_all_post_data(post_list)
    FormatLogger.info("Database", "Write all spider data to database finished!")

    FormatLogger.info("Database", "Prepare all post data for word split......")
    # 查询已有数据
    process_post_list: list[PostDataContent]
    search_key_id: int
    process_post_list, search_key_id = query_all_post_and_comment_by_keyword(post_list[0].search_key)

    process_list = [(item.content, *item.comments) for item in process_post_list]
    process_list = [string for item in process_list for string in item]
    FormatLogger.info("Database", "Prepare all post data for word split finished!")

    FormatLogger.info("WordSplit", "Start word spilt for all post data......")
    if MULTI_PROCESS_JIEBA:
        process_result = parallel_function_with_waiting_result(word_split, process_list)
    else:
        process_result = []
        for word in process_list:
            process_result.append(word_split(word))
    FormatLogger.info("WordSplit", "Finish word spilt for all post data!")

    FormatLogger.info("WordSplit", "Start collect word split result")
    word_dict = dict()
    for word_split_result in process_result:
        for key, count in word_split_result.items():
            if key not in word_dict:
                word_dict[key] = count
            else:
                word_dict[key] += count

    spilt_result_list: list[WordFrequency] = []
    for word, final_result in word_dict.items():
        frequency = WordFrequency(search_key_id, word, final_result)
        spilt_result_list.append(frequency)
    FormatLogger.info("WordSplit", "Finish collect word split result!")

    FormatLogger.info("Database", "Writing all word split data to database......")
    insert_all_word_split_data(spilt_result_list)
    FormatLogger.info("Database", "Write all word split data to database finished!")
