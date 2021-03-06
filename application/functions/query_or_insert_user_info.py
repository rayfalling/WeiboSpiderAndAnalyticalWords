from sqlalchemy import or_
from sqlalchemy.orm import scoped_session

from libs import FormatLogger, UserData
from ..core import db
from ..database_model import UserInfo

__all__ = (
    "query_user_login", "query_user_info", "update_user_info", "insert_user_register", "query_user_info_by_keyword"
)


def query_user_login(user: UserData, password: str) -> UserData:
    """
    查询用户是否可以登录

    :param user: 用户信息
    :param password: 用户密码
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(UserInfo).filter(
        UserInfo.username == user.username, UserInfo.password == password
    ).all()
    session.close()

    if len(result) != 1:
        FormatLogger.warning(
            "Database", "Multi user exist in database or user not exist. Username: {}".format(user.username)
        )
        user.username = "-1"
        return user
    else:
        user.avatar = result[0].avatar
        user.username = result[0].username
        user.nickname = result[0].nickname
        user.user_type = result[0].user_type
        return user


def query_user_info(user: UserData) -> UserData:
    """
    查询用户信息

    :param user: 用户信息
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(UserInfo).filter(UserInfo.username == user.username).all()
    session.close()

    if len(result) != 1:
        FormatLogger.warning(
            "Database", "Multi user exist in database or user not exist. Username: {}".format(user.username)
        )
        user.username = "-1"
        return user
    else:
        user.avatar = result[0].avatar
        user.username = result[0].username
        user.nickname = result[0].nickname
        return user


def query_user_info_by_keyword(keyword: str) -> str:
    """
    查询用户信息

    :param keyword: 查询信息
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(UserInfo).filter(
        or_(UserInfo.username == keyword, UserInfo.nickname == keyword)
    ).first()

    if result is None:
        session.close()
        return "-1"
    else:
        username = result.username
        session.close()
        return username


def update_user_info(user: UserData, password_old: str, password_new: str) -> bool:
    """
    更新用户信息

    :param user: 用户信息
    :param password_old: 用户密码旧
    :param password_new: 用户密码新
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(UserInfo).filter(UserInfo.username == user.username).all()

    if len(result) <= 0:
        FormatLogger.warning(
            "Database", "Update user info in database failed. User not exist. Username: {}".format(user.username)
        )
        session.close()
        return False
    elif result[0].password != password_old:
        FormatLogger.warning(
            "Database", "Update user info in database failed. Password mismatch. Username: {}".format(user.username)
        )
        session.close()
        return False
    else:
        result[0].password = password_new
        result[0].nickname = user.nickname
        session.commit()

        user.avatar = result[0].avatar
        user.nickname = result[0].nickname

        session.close()
        return True


def insert_user_register(user: UserData, password: str) -> bool:
    """
    查询用户是否可以登录

    :param user: 用户信息
    :param password: 用户密码
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(UserInfo).filter(
        or_(UserInfo.username == user.username, UserInfo.nickname == user.nickname)
    ).all()

    session.close()

    if len(result) > 0:
        FormatLogger.warning(
            "Database", "Username or nickname already exist in database. Username: {}".format(user.username)
        )
        return False
    else:
        user_info = UserInfo(user.username, user.nickname, password, user.avatar, user.user_type)
        session.add(user_info)
        session.commit()

        return True
