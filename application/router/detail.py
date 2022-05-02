import json

from flask import Blueprint, request, jsonify

from libs import FormatLogger
from .common import process_after_request, process_login_status
from ..functions import query_post_detail_by_id


detail_router = Blueprint("detail", __name__)
detail_router.before_request(process_login_status)
detail_router.after_request(process_after_request)


# noinspection DuplicatedCode
@detail_router.route("/api/post/detail", methods=["POST"])
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
        FormatLogger.error("PostRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_post_id = request_json.get("PostId", -1)

    if request_post_id == -1:
        FormatLogger.error("PostRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    result = query_post_detail_by_id(request_post_id)

    if result.post_id == -1:
        response_data["status"] = -1
        response_data["message"] = "查询错误，源微博不存在"
        response_data["data"] = {
            "result": {}
        }
    else:
        response_data["status"] = 0
        response_data["message"] = "查询成功"
        response_data["data"] = {
            "result": []
        }

        response_data["data"]["result"] = {
            "tags": result.tags,
            "id": result.post_id,
            "content": result.content,
            "username": result.username,
            "comments": result.comments,
            "reposts_count": result.reposts_count,
            "comments_count": result.comments_count,
            "attitudes_count": result.attitudes_count,
            "time": result.time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    return jsonify(response_data)
