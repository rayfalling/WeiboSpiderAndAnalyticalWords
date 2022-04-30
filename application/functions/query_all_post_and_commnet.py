from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderSearchKey, SpiderOriginPostData, SpiderOriginCommentData

from libs import FormatLogger
from libs.data_model import PostDataContent

__all__ = ("query_all_post_and_comment_by_keyword",)


def query_all_post_and_comment_by_keyword(keyword: str, modify_list=None) -> tuple:
    """
    通过搜索关键词查询目前所有的微博和评论

    :param modify_list:
    :param keyword:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    result = session.query(SpiderSearchKey).filter(SpiderSearchKey.key == keyword).all()

    if len(result) == 0:
        FormatLogger.error("Database", "Search key not in database.")
        return None, -1
    else:
        search_key_id = result[0].id

    return query_post(session=session, search_key_id=search_key_id, update_list=modify_list), search_key_id


def query_post(session: scoped_session, search_key_id: int, update_list=None):
    """
    查询所有的微博数据

    :param update_list:
    :param session: 数据库连接会话
    :param search_key_id: 关键词的Id
    :return:
    """
    if update_list is None:
        update_list = []

    if len(update_list) == 0:
        result = session.query(SpiderOriginPostData).filter(
            SpiderOriginPostData.search_key_id == search_key_id
        ).with_entities(SpiderOriginPostData.id, SpiderOriginPostData.content).all()
    else:
        result = session.query(SpiderOriginPostData).filter(
            SpiderOriginPostData.search_key_id == search_key_id,
            SpiderOriginPostData.id.in_(update_list)
        ).with_entities(SpiderOriginPostData.id, SpiderOriginPostData.content).all()

    post_list: list[PostDataContent] = []

    for item in result:
        post_list.append(PostDataContent(item.id, item.content, query_comment(session, item.id)))

    return post_list


def query_comment(session: scoped_session, post_id: int):
    """
    查询所有的微博数据

    :param session: 数据库连接会话
    :param post_id: 数据库储存的帖子的Id
    :return:
    """
    result = session.query(SpiderOriginCommentData).filter(
        SpiderOriginCommentData.post_id == post_id
    ).with_entities(SpiderOriginCommentData.content).all()

    return [item.content for item in result]
