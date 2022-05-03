from datetime import datetime

from sqlalchemy.orm import scoped_session

from libs import FormatLogger
from ..core import db
from ..database_model import UserInfo, UserHistory, UserCollect

__all__ = ("insert_user_history", "query_user_collect", "insert_user_collect", "delete_user_collect",)


# noinspection DuplicatedCode
def insert_user_history(username: str, post_id: int) -> bool:
    """
    插入用户浏览数据

    :param username: 用户名
    :param post_id: 浏览的贴子Id
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    if user_id == -1:
        return False

    history_list = session.query(UserHistory).filter(
        UserHistory.user_id == user_id, UserHistory.post_id == post_id
    ).all()

    if len(history_list) < 1:
        history = UserHistory(user_id, post_id, datetime.now())
        session.add(history)
    else:
        history_list[0].update_time()

    session.commit()
    session.close()
    return True


# noinspection DuplicatedCode
def query_user_collect(username: str, post_id: int) -> tuple[bool, bool]:
    """
    插入用户浏览数据

    :param username: 用户名
    :param post_id: 浏览的贴子Id
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    if user_id == -1:
        return False, False

    collect_list = session.query(UserCollect).filter(
        UserCollect.user_id == user_id, UserCollect.post_id == post_id
    ).all()

    session.commit()
    session.close()
    return True, len(collect_list) == 1


# noinspection DuplicatedCode
def insert_user_collect(username: str, post_id: int) -> tuple[bool, bool]:
    """
    插入用户浏览数据

    :param username: 用户名
    :param post_id: 浏览的贴子Id
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    if user_id == -1:
        return False, False

    collect_list = session.query(UserCollect).filter(
        UserCollect.user_id == user_id, UserCollect.post_id == post_id
    ).all()

    if len(collect_list) == 1:
        return True, False

    collect = UserCollect(user_id=user_id, post_id=post_id)
    session.add(collect)
    session.commit()
    session.close()
    return True, True


# noinspection DuplicatedCode
def delete_user_collect(username: str, post_id: int) -> tuple[bool, bool]:
    """
    插入用户浏览数据

    :param username: 用户名
    :param post_id: 浏览的贴子Id
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    if user_id == -1:
        return False, False

    collect_list = session.query(UserCollect).filter(
        UserCollect.user_id == user_id, UserCollect.post_id == post_id
    ).all()

    if len(collect_list) == 0:
        return True, False

    session.delete(collect_list[0])
    session.commit()
    session.close()
    return True, True


def query_user_id(session: scoped_session, username: str) -> int:
    """
    查询用户Id

    :param session:
    :param username:
    :return:
    """
    result = session.query(UserInfo).filter(UserInfo.username == username).all()

    if len(result) == 0:
        FormatLogger.warning(
            "Database", "User not exist in database. Username: {}".format(username)
        )
        return -1

    return result[0].id
