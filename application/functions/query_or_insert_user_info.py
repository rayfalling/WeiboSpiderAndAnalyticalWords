from sqlalchemy import or_
from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import UserInfo

from libs import FormatLogger, UserData

__all__ = ("query_user_login", "insert_user_register")


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
