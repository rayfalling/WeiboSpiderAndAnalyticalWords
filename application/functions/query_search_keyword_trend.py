import typing

from sqlalchemy.orm import scoped_session

from .query_search_key import query_search_key_id

from ..core import db
from ..database_model import SpiderSearchKey, SpiderOriginPostData, SpiderOriginCommentData

from libs import FormatLogger, TagTrend

__all__ = ("query_search_key_trend",)


def query_search_key_trend(key: str) -> typing.Optional[dict[str, TagTrend]]:
    """
    获取当前搜索关键词热度

    :param key: 搜索关键词
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    key_id = query_search_key_id(key)

    if key_id == -1:
        return None

    result: list[SpiderOriginPostData] = session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.search_key_id == key_id, SpiderOriginPostData.tags != ""
    ).all()

    update_immediately = True if len(result) < 50 else False

    result_dict: dict[str, TagTrend] = {}
    for item in result:
        if item.tags == "":
            continue

        tag_list = item.tags.split("#")
        for tag in tag_list:
            if tag not in result_dict:
                result_dict[tag] = TagTrend(tag)

            result_dict[tag].add_post(
                item.user_id, item.attitudes_count, item.comments_count, item.reposts_count, update_immediately
            )

    for key, value in result_dict.items():
        value.update_trend()

    return result_dict
