from flask import request, session, abort

__all__ = ("process_after_request", "process_login_status", )


def process_after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


def process_login_status():
    """
    检查是否有登录状态
    :return:
    """

    if session.get("login_status") is None or not session.get("login_status"):
        return abort(401)

    session.permanent = True
    return
