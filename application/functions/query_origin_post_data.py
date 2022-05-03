from sqlalchemy import and_, or_
from sqlalchemy.orm import scoped_session

from utils import split_tags
from ..core import db
from ..database_model import SpiderOriginPostData, SpiderOriginCommentData

from libs import FormatLogger, SearchResult, PostDetail

__all__ = ("query_search_by_keyword", "query_post_detail_by_id", )


def query_search_by_keyword(keyword: str) -> list[SearchResult]:
    """
    查询搜索关键词

    :param keyword: 搜索关键词
    :return:
    """
    search_list = keyword.split(" ")
    FormatLogger.debug("Database", "Search keyword is {}".format(search_list))

    filter_tag_rule = or_(*[SpiderOriginPostData.tags.like("%" + word + "%") for word in search_list])
    filter_content_rule = or_(*[SpiderOriginPostData.content.like("%" + word + "%") for word in search_list])

    session: scoped_session = db.create_scoped_session(None)
    result = session.query(SpiderOriginPostData).filter(or_(filter_tag_rule, filter_content_rule)).all()

    session.close()

    search_result_list = []
    for item in result:
        tags = split_tags(item.tags)
        search_result = SearchResult(item.id, tags, item.content, item.time)
        search_result_list.append(search_result)

    search_result_list.sort(key=lambda rs: rs.time, reverse=True)
    return search_result_list


def query_post_detail_by_id(post_id: int) -> PostDetail:
    """
    查询搜索关键词

    :param post_id: 搜索关键词
    :return:
    """
    FormatLogger.debug("Database", "Query detail id is {}".format(post_id))

    session: scoped_session = db.create_scoped_session(None)
    result = session.query(SpiderOriginPostData).filter(SpiderOriginPostData.id == post_id).all()

    if len(result) == 0:
        FormatLogger.debug("Database", "Query detail id is {}".format(post_id))
        return PostDetail(-1)

    item = result[0]
    tags = split_tags(item.tags)

    count = (item.attitudes_count, item.comments_count, item.reposts_count)
    comment_result = session.query(SpiderOriginCommentData).filter(SpiderOriginCommentData.post_id == post_id).all()

    comments = []
    for comment in comment_result:
        comments.append(comment.content)

    session.close()

    return PostDetail(item.id, item.username, tags, item.content, item.time, count, comments)
