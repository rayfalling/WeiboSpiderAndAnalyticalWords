import json

from flask import Blueprint, request, jsonify

from libs import FormatLogger
from .common import process_after_request, process_login_status
from ..functions import query_search_by_keyword


search_router = Blueprint("search", __name__)
search_router.before_request(process_login_status)
search_router.after_request(process_after_request)


# noinspection DuplicatedCode
@search_router.route("/api/search", methods=["POST"])
def request_login():
    """
    路由--搜索资讯

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("UserRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_keyword = request_json.get("Keyword", "")

    if request_keyword == "":
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    result = query_search_by_keyword(request_keyword)

    response_data["status"] = 0
    response_data["message"] = "查询成功"
    response_data["data"] = {
        "result": []
    }

    for item in result:
        response_data["data"]["result"].append({
            "id": item.post_id,
            "tags": item.tags,
            "time": item.time,
            "content": item.content
        })

    return jsonify(response_data)
