import json
import random

from flask import Blueprint, request, jsonify, session

from .common import process_after_request

from ..functions import query_user_login, insert_user_register

from libs import FormatLogger, UserData

user_router = Blueprint("user", __name__)
user_router.after_request(process_after_request)

__all__ = ("user_router",)


# noinspection DuplicatedCode
@user_router.route("/api/login", methods=["POST"])
def request_login():
    """
    路由--请求登录

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
    request_username = request_json.get("Username", "")
    request_password = request_json.get("Password", "")

    if request_username == "" or request_password == "":
        FormatLogger.error("AdminRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    user: UserData = UserData(request_username, "", "", -1)
    user = query_user_login(user, request_password)

    if user.username == "-1":
        response_data["status"] = -1
        response_data["message"] = "用户名或密码错误"
        response_data["data"] = {}
    else:
        response_data["status"] = 0
        response_data["message"] = "登录成功"
        response_data["data"] = {
            "avatar": user.avatar,
            "username": user.username,
            "nickname": user.nickname,
            "user_type": user.user_type,
        }

        session["login_status"] = True

        session["avatar"] = user.avatar
        session["username"] = user.username
        session["nickname"] = user.nickname
        session["user_type"] = user.user_type

    return jsonify(response_data)


# noinspection DuplicatedCode
@user_router.route("/api/register", methods=["POST"])
def request_register():
    """
    路由--请求注册

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
    request_username = request_json.get("Username", "")
    request_nickname = request_json.get("Nickname", "")
    request_password = request_json.get("Password", "")

    if request_username == "" or request_password == "" or request_nickname == "":
        FormatLogger.error("UserRouter", "Empty request data! Request url is {}".format(request.url))
        response_data["message"] = "参数错误"
        return jsonify(response_data)

    avatar_index = int(random.random() * 100) % 5 + 1
    avatar_url = f"static/avatar{avatar_index}.png"

    user: UserData = UserData(request_username, request_nickname, avatar_url, 1)
    result = insert_user_register(user, request_password)

    if not result:
        response_data["status"] = -1
        response_data["message"] = "用户已存在"
        response_data["data"] = {}
    else:
        response_data["status"] = 0
        response_data["message"] = "注册成功"
        response_data["data"] = {}

    return jsonify(response_data)


@user_router.route("/api/login/status", methods=["POST"])
def query_login():
    """
    路由--检查是否有登录状态

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

    if session.get("login_status") is None or not session.get("login_status"):
        response_data["status"] = -1
        response_data["message"] = "用户未登录"
    else:
        response_data["status"] = 0
        response_data["message"] = "用户已登录"
        response_data["data"] = {
            "avatar": session["avatar"],
            "username": session["username"],
            "nickname": session["nickname"],
            "user_type": session["user_type"],
        }

    return jsonify(response_data)
