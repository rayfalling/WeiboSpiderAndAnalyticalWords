from sqlalchemy import and_, or_
from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderOriginPostData

from libs import FormatLogger, SearchResult

__all__ = ("query_search_by_keyword",)


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

    search_result_list = []
    for item in result:
        search_result = SearchResult(item.id, item.tags, item.content, item.time)
        search_result_list.append(search_result)

    sorted(search_result_list, key=lambda rs: rs.time, reverse=True)
    return search_result_list
