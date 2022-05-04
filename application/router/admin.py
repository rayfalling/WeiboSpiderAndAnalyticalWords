import json

from flask import Blueprint, request, jsonify, session

from config import Config
from libs import fetch_pages, FormatLogger, word_split
from libs.data_model import PostData, PostDataContent, WordFrequency

from .common import process_after_request, process_login_status

from ..thread_pool import submit_function_async
from ..functions import clear_all_data, insert_all_post_data, delete_post_with_id, query_user_info_by_keyword
from ..functions import insert_all_word_split_data, query_all_post_and_comment_by_keyword, delete_comment_with_id

admin_router = Blueprint("admin", __name__)
admin_router.before_request(process_login_status)
admin_router.after_request(process_after_request)

__all__ = ("admin_router",)


# noinspection DuplicatedCode
@admin_router.route("/api/admin/spider/update", methods=["POST"])
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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    clear_all_data()

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_pages = request_json.get("Pages", 0)
    request_keyword = request_json.get("Keyword", "")

    # save to config
    Config.SEARCH_KEYWORD = request_keyword

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


# noinspection DuplicatedCode
@admin_router.route("/api/admin/post/delete", methods=["POST"])
def request_post_delete():
    """
    路由--删除微博数据

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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_post_id = request_json.get("PostId", -1)

    if request_post_id == -1:
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    result = delete_post_with_id(request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "删除失败"
    else:
        response_data["status"] = 0
        response_data["message"] = "删除成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@admin_router.route("/api/admin/comment/delete", methods=["POST"])
def request_comment_delete():
    """
    路由--删除微博数据

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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_post_id = request_json.get("PostId", -1)
    request_comment_id = request_json.get("CommentId", -1)

    if request_comment_id == -1 or request_post_id == -1:
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    result, search_key = delete_comment_with_id(request_post_id, request_comment_id)

    # 异步线程开始处理分词结果
    submit_function_async(process_word_split, search_key, [request_post_id])

    if not result:
        response_data["status"] = -1
        response_data["message"] = "删除失败"
    else:
        response_data["status"] = 0
        response_data["message"] = "删除成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@admin_router.route("/api/admin/word_trend/update", methods=["POST"])
def request_word_trend_update():
    """
    路由--更新热度趋势配置

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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_trend_hour = request_json.get("TrendHour", -1)
    request_trend_count = request_json.get("TrendCount", -1)
    request_predict_count = request_json.get("PredictCount", -1)

    if request_trend_hour < 0 or request_trend_count < 0 or request_predict_count < 0:
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    # save to config
    Config.TREND_CYCLE_HOUR = request_trend_hour
    Config.TREND_CYCLE_COUNT = request_trend_count
    Config.TREND_PREDICT_COUNT = request_predict_count

    response_data["status"] = 0
    response_data["message"] = "保存成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@admin_router.route("/api/admin/word_cloud/update", methods=["POST"])
def request_word_cloud_update():
    """
    路由--更新词云配置参数

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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_word_cloud_count = request_json.get("WordCloudCount", -1)

    if request_word_cloud_count < 0:
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    # save to config
    Config.WORD_CLOUD_LIMIT_COUNT = request_word_cloud_count

    response_data["status"] = 0
    response_data["message"] = "保存成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@admin_router.route("/api/admin/user/query", methods=["POST"])
def request_query_user():
    """
    路由--查询用户信息

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

    if session.get("user_type") is None or session.get("user_type") == 1:
        FormatLogger.error("AdminRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "用户不是管理员"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_keyword = request_json.get("Keyword", "")

    if request_keyword == "":
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    result = query_user_info_by_keyword(request_keyword)

    if result == "-1":
        response_data["status"] = -1
        response_data["message"] = "用户不存在"
    else:
        response_data["status"] = 0
        response_data["message"] = "查询成功"
        response_data["data"] = {
            "username": result
        }

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
    post_modify_list = insert_all_post_data(post_list)
    FormatLogger.info("Database", "Write all spider data to database finished!")
    process_word_split(post_list[0].search_key, post_modify_list)


def process_word_split(search_key: str, post_modify_list: list[int]):
    """
    刷新分词数据

    :param search_key:
    :param post_modify_list:
    :return:
    """
    FormatLogger.info("Database", "Prepare all post data for word split......")
    # 查询已有数据
    process_post_list: list[PostDataContent]
    search_key_id: int
    process_post_list, search_key_id = query_all_post_and_comment_by_keyword(search_key, post_modify_list)

    process_list = [(item.id, [item.content, *item.comments]) for item in process_post_list]
    process_list = [(item[0], string) for item in process_list for string in item[1]]
    FormatLogger.info("Database", "Prepare all post data for word split finished!")

    FormatLogger.info("WordSplit", "Start word spilt for post data......")
    spilt_result_list: list[WordFrequency] = []
    for item in process_list:
        process_result = word_split(item[1])

        for key, value in process_result.items():
            frequency = WordFrequency(search_key_id, item[0], key, value[0], value[1])
            spilt_result_list.append(frequency)
    FormatLogger.info("WordSplit", "Finish word spilt for post data!")

    FormatLogger.info("Database", "Writing all word split data to database......")
    insert_all_word_split_data(spilt_result_list)
    FormatLogger.info("Database", "Write all word split data to database finished!")
