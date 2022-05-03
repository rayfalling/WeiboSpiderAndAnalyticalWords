from datetime import datetime

from sqlalchemy.orm import scoped_session

from libs import FormatLogger, UserActivity
from utils import split_tags
from ..core import db
from ..database_model import UserInfo, UserHistory, UserCollect, SpiderOriginPostData

__all__ = (
    "insert_user_history", "query_user_history_all", "delete_user_history",
    "query_user_collect", "insert_user_collect", "delete_user_collect", "query_user_collect_all"
)


# noinspection DuplicatedCode
def query_user_history_all(username: str) -> list[UserActivity]:
    """
    查询用户浏览数据

    :param username: 用户名
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    history_list: list[UserHistory] = session.query(UserHistory).filter(UserHistory.user_id == user_id).all()

    result_list: list[UserActivity] = []
    for history in history_list:
        post = query_post_by_id(session=session, post_id=history.post_id)
        if post is None:
            continue

        tags = split_tags(post.tags)
        activity = UserActivity(history.post_id, tags, post.content, post.time, history.time)
        result_list.append(activity)

    result_list.sort(key=lambda result: result.activity_time, reverse=True)
    session.close()
    return result_list


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
def delete_user_history(username: str, post_id: int) -> tuple[bool, bool]:
    """
    删除用户浏览记录

    :param username: 用户名
    :param post_id: 浏览的贴子Id
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    if user_id == -1:
        return False, False

    collect_list = session.query(UserHistory).filter(
        UserHistory.user_id == user_id, UserHistory.post_id == post_id
    ).all()

    if len(collect_list) == 0:
        return True, False

    session.delete(collect_list[0])
    session.commit()
    session.close()
    return True, True


# noinspection DuplicatedCode
def query_user_collect_all(username: str) -> list[UserActivity]:
    """
    查询用户收藏数据

    :param username: 用户名
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    user_id = query_user_id(session=session, username=username)

    history_list: list[UserCollect] = session.query(UserCollect).filter(UserCollect.user_id == user_id).all()

    result_list: list[UserActivity] = []
    for collect in history_list:
        post = query_post_by_id(session=session, post_id=collect.post_id)
        if post is None:
            continue

        tags = split_tags(post.tags)
        activity = UserActivity(collect.post_id, tags, post.content, post.time, collect.id)
        result_list.append(activity)

    result_list.sort(key=lambda result: result.activity_time, reverse=True)
    session.close()
    return result_list


# noinspection DuplicatedCode
def query_user_collect(username: str, post_id: int) -> tuple[bool, bool]:
    """
    查询用户是否收藏

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
    删除用户收藏数据

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


def query_post_by_id(session: scoped_session, post_id: int):
    """
    查询微博数据

    :param session:
    :param post_id:
    :return:
    """
    return session.query(SpiderOriginPostData).filter(SpiderOriginPostData.id == post_id).first()
