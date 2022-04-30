import typing

from sqlalchemy.orm import scoped_session

from . import query_or_insert_search_key_id

from ..core import db
from ..database_model import SpiderOriginPostData, SpiderOriginCommentData

from libs import FormatLogger
from libs.data_model import PostData, CommentData

__all__ = ("insert_all_post_data",)


def insert_all_post_data(post_data_list: typing.List[PostData]) -> list[int]:
    """
    将爬虫结果写入数据库
    全量查询一次数据库, 获取当前数据库内容副本, 再次去重

    :param post_data_list: 爬虫获取的数据结果
    :return:
    """
    if len(post_data_list) == 0:
        return []

    search_key = post_data_list[0].search_key
    search_key_id = query_or_insert_search_key_id(search_key)

    session: scoped_session = db.create_scoped_session(None)
    database_post_data: list[SpiderOriginPostData] = query_all_post(session)
    mid: list[int] = [item.mid for item in database_post_data]

    post_modify_list = []
    for item in post_data_list:
        if item.mid in mid:
            find_data = next((data for data in database_post_data if data.mid == item.mid), None)

            if None is find_data:
                continue

            insert_comment_data(session, find_data.id, item.comment)
            post_modify_list.append(find_data.id)
        else:
            if item.search_key != search_key:
                FormatLogger.error("Database", "Search key not equal in post_data_list, skipping...")
                continue

            data_id = insert_post_data(session, item, search_key_id)
            post_modify_list.append(data_id)
    session.commit()

    return post_modify_list


def insert_post_data(session: scoped_session, post_data: PostData, key_id: int):
    """
    将单条数据写入数据库

    :param session: 数据库连接会话
    :param post_data: 提交数据
    :param key_id: 搜索关键词Id
    :return:
    """
    origin_data = SpiderOriginPostData(post_data, key_id)
    session.add(origin_data)
    session.commit()
    insert_comment_data(session, origin_data.id, post_data.comment)
    return origin_data.id


def insert_comment_data(session: scoped_session, post_id: int, comment_data: CommentData):
    """
    将单条数据写入数据库

    :param session: 数据库连接会话
    :param post_id: 微博评论对应ID
    :param comment_data: 提交数据
    :return:
    """
    database_comment_data: list[SpiderOriginCommentData] = query_comment_with_id(session, post_id)
    comment_id_list: list[int] = [item.comment_id for item in database_comment_data]

    for key, content in comment_data.comment.items():
        if key in comment_id_list:
            find_data = next((data for data in database_comment_data if data.comment_id == key), None)

            if None is find_data:
                continue

            # 更新评论数据
            find_data.content = content
        else:
            origin_data = SpiderOriginCommentData(post_id, key, content)
            session.add(origin_data)

    # 提交评论数据
    session.commit()


def query_all_post(session: scoped_session) -> list[SpiderOriginPostData]:
    """
    获取当前所有微博帖子数据

    :return:
    """
    return session.query(SpiderOriginPostData).all()


def query_comment_with_id(session: scoped_session, post_id: int) -> list[SpiderOriginCommentData]:
    """
    获取当前所有的评论数据

    :return:
    """
    return session.query(SpiderOriginCommentData).filter(SpiderOriginCommentData.post_id == post_id).all()
