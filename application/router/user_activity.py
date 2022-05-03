import json

from flask import Blueprint, request, jsonify, session, abort

from libs import FormatLogger, UserData
from .common import process_after_request, process_login_status
from ..functions import query_user_info, insert_user_history
from ..functions import query_user_collect, insert_user_collect, delete_user_collect

user_activity_router = Blueprint("user_activity", __name__)
user_activity_router.before_request(process_login_status)
user_activity_router.after_request(process_after_request)

__all__ = ("user_activity_router",)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/info", methods=["POST"])
def request_user_info():
    """
    路由--请求用户信息

    :return:
    """
    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

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
    request_username = request_json.get("Username", "")

    if request_username == "" or session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    user: UserData = UserData(request_username, "", "", -1)
    user = query_user_info(user)

    if user.username == "-1":
        response_data["status"] = -1
        response_data["message"] = "用户信息查询失败"
    else:
        response_data["status"] = 0
        response_data["message"] = "登录成功"
        response_data["data"] = {
            "avatar": user.avatar,
            "username": user.username,
            "nickname": user.nickname,
        }

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/history/add", methods=["POST"])
def request_user_history_add():
    """
    路由--添加用户浏览记录

    :return:
    """
    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

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
    request_post_id = request_json.get("PostId", -1)
    request_username = request_json.get("Username", "")

    if request_username == "" or request_post_id == -1:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result = insert_user_history(request_username, request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "发生了一些内部错误"
    else:
        response_data["status"] = 0
        response_data["message"] = "记录浏览历史成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/collect/status", methods=["POST"])
def request_user_collect_status():
    """
    路由--获取用户收藏状态

    :return:
    """
    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

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
    request_post_id = request_json.get("PostId", -1)
    request_username = request_json.get("Username", "")

    if request_username == "" or request_post_id == -1:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result, status = query_user_collect(request_username, request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "用户未收藏"
    else:
        response_data["status"] = 0
        response_data["message"] = "用户已收藏"
        response_data["data"] = {
            "collect": status
        }

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/collect/add", methods=["POST"])
def request_user_collect_add():
    """
    路由--添加用户收藏

    :return:
    """
    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

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
    request_post_id = request_json.get("PostId", -1)
    request_username = request_json.get("Username", "")

    if request_username == "" or request_post_id == -1:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result, status = insert_user_collect(request_username, request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "内部错误"
    else:
        if not status:
            response_data["status"] = -1
            response_data["message"] = "用户已收藏"
        else:
            response_data["status"] = 0
            response_data["message"] = "收藏成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/collect/remove", methods=["POST"])
def request_user_collect_remove():
    """
    路由--取消用户收藏

    :return:
    """
    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

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
    request_post_id = request_json.get("PostId", -1)
    request_username = request_json.get("Username", "")

    if request_username == "" or request_post_id == -1:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result, status = delete_user_collect(request_username, request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "内部错误"
    else:
        if not status:
            response_data["status"] = -1
            response_data["message"] = "用户未收藏"
        else:
            response_data["status"] = 0
            response_data["message"] = "收藏成功"

    return jsonify(response_data)
