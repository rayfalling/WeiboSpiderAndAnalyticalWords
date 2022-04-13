import json

from flask import Blueprint, request, jsonify
from libs import fetch_pages, FormatLogger

from .common import process_after_request
from ..functions import insert_all_data

admin_router = Blueprint("admin", __name__)
admin_router.after_request(process_after_request)

__all__ = ("admin_router",)


# 请求爬虫更新
@admin_router.route("/admin/spider/update", methods=["POST"])
def request_spider_update():
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

    success_count = insert_all_data(result)
    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"] = {
        "count": success_count
    }

    return jsonify(response_data)
