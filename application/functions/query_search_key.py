from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderSearchKey

from libs import FormatLogger

__all__ = ("query_or_insert_search_key_id", "query_search_key_id")


def query_or_insert_search_key_id(key: str):
    """
    获取搜索关键词ID

    :param key: 搜索关键词
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = query_comment_with_id(session, key)

    if len(result) > 1:
        FormatLogger.warning("Database", "Multi search key in database.")
        search_key_id = result[0].id
    elif len(result) == 0:
        origin_data = SpiderSearchKey(key)
        session.add(origin_data)
        session.commit()
        search_key_id = origin_data.id
    else:
        search_key_id = result[0].id

    return search_key_id


def query_search_key_id(key: str):
    """
    获取搜索关键词ID

    :param key: 搜索关键词
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = query_comment_with_id(session, key)

    if len(result) > 1:
        FormatLogger.warning("Database", "Multi search key in database.")
        search_key_id = result[0].id
    elif len(result) == 0:
        FormatLogger.warning("Database", "Can't find search key in database.")
        search_key_id = -1
    else:
        search_key_id = result[0].id

    return search_key_id


def query_comment_with_id(session: scoped_session, key: str) -> list[SpiderSearchKey]:
    """
    获取当前所有的评论数据

    :param session: 会话session
    :param key: 搜索关键词
    :return:
    """
    return session.query(SpiderSearchKey).filter(SpiderSearchKey.key == key).all()
