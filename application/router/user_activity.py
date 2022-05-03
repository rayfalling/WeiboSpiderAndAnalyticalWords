import json

from flask import Blueprint, request, jsonify, session, abort

from libs import FormatLogger, UserData
from .common import process_after_request, process_login_status
from ..functions import query_user_info, insert_user_history, update_user_info
from ..functions import query_user_collect, insert_user_collect, delete_user_collect
from ..functions import query_user_history_all, query_user_collect_all, delete_user_history

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
@user_activity_router.route("/api/user/info/update", methods=["POST"])
def request_user_update():
    """
    路由--更新用户信息

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
    request_nickname = request_json.get("Nickname", "")
    request_password_old = request_json.get("PasswordOld", "")
    request_password_new = request_json.get("PasswordNew", "")

    if request_username == "" or session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    if request_password_new == "" or request_password_old == "" or request_nickname == "":
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "参数无效"
        return jsonify(response_data)

    user: UserData = UserData(request_username, request_nickname, "", -1)
    result = update_user_info(user, request_password_old, request_password_new)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "更新用户信息失败, 旧密码不正确"
    else:
        response_data["status"] = 0
        response_data["message"] = "更新成功"
        response_data["data"] = {
            "avatar": user.avatar,
            "username": user.username,
            "nickname": user.nickname,
        }

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/history/all", methods=["POST"])
def request_user_history_all():
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
    request_limit = request_json.get("Limit", -1)
    request_username = request_json.get("Username", "")

    if request_username == "":
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result = query_user_history_all(request_username)

    result_list = []
    for item in result:
        result_list.append({
            "id": item.post_id,
            "tags": item.tags,
            "content": item.content,
            "time": item.time.strftime("%Y-%m-%d %H:%M:%S"),
            "activity_time": item.activity_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    response_data["status"] = 0
    response_data["message"] = "查询成功"
    if request_limit == -1:
        response_data["data"]["result"] = result_list
    else:
        response_data["data"]["result"] = result_list[:request_limit]

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
@user_activity_router.route("/api/user/history/remove", methods=["POST"])
def request_user_history_remove():
    """
    路由--取消用户历史

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

    result, status = delete_user_history(request_username, request_post_id)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "内部错误"
    else:
        if not status:
            response_data["status"] = -1
            response_data["message"] = "无历史记录"
        else:
            response_data["status"] = 0
            response_data["message"] = "删除历史成功"

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_activity_router.route("/api/user/collect/all", methods=["POST"])
def request_user_collect_all():
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
    request_limit = request_json.get("Limit", -1)
    request_username = request_json.get("Username", "")

    if request_username == "":
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "请求参数错误"
        return jsonify(response_data)

    if session["username"] != request_username:
        FormatLogger.error("UserRouter", "Error request data! Request url is {}".format(request.url))
        response_data["message"] = "用户登录信息无效"
        return jsonify(response_data)

    result = query_user_collect_all(request_username)

    result_list = []
    for item in result:
        result_list.append({
            "id": item.post_id,
            "tags": item.tags,
            "content": item.content,
            "time": item.time.strftime("%Y-%m-%d %H:%M:%S"),
            "activity_time": item.activity_time,
        })

    response_data["status"] = 0
    response_data["message"] = "查询成功"
    if request_limit == -1:
        response_data["data"]["result"] = result_list
    else:
        response_data["data"]["result"] = result_list[:request_limit]

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
            response_data["message"] = "删除收藏成功"

    return jsonify(response_data)
