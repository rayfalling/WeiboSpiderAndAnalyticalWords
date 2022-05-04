from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderSearchKey, SpiderOriginPostData, WordSpiltResult

from config import Config
from libs import FormatLogger, TagTrend
from libs.data_model import WordFrequencySummary

__all__ = (
    "query_all_word_cloud", "query_all_word_cloud_by_search_key",
    "query_word_cloud_trend", "query_word_cloud_trend_by_search_key",
    "query_word_cloud_hot_trend", "query_word_cloud_hot_trend_by_search_key",
)


def query_all_word_cloud(keyword: str = Config.SEARCH_KEYWORD,
                         limit: int = Config.WORD_CLOUD_LIMIT_COUNT) -> list[WordFrequencySummary]:
    """
    通过搜索关键词查询词云数据

    :param keyword:
    :param limit:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    search_key = session.query(SpiderSearchKey).filter(SpiderSearchKey.key == keyword).first()

    if search_key is None:
        FormatLogger.error("Database", "Search key not in database.")
        return []

    split_list: list[WordSpiltResult] = session.query(WordSpiltResult).filter(
        WordSpiltResult.search_key_id == search_key.id
    ).all()

    return sum_word_frequency(split_list, limit)


def query_all_word_cloud_by_search_key(keyword: str = Config.SEARCH_KEYWORD,
                                       limit: int = Config.WORD_CLOUD_LIMIT_COUNT) -> list[WordFrequencySummary]:
    """
    通过搜索关键词查询词云数据

    :param keyword:
    :param limit:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    post_list = query_post_search_by_keyword(session, keyword)

    split_list: list[WordSpiltResult] = session.query(WordSpiltResult).filter(
        WordSpiltResult.post_id.in_(post_list)
    ).all()
    session.close()

    return sum_word_frequency(split_list, limit)


def query_word_cloud_trend(keyword: str = Config.SEARCH_KEYWORD) -> dict[str, list[WordFrequencySummary]]:
    """
    通过搜索关键词查询词云数据

    :param keyword:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    search_key = session.query(SpiderSearchKey).filter(SpiderSearchKey.key == keyword).first()

    if search_key is None:
        FormatLogger.error("Database", "Search key not in database.")
        return {
            "decrease": [],
            "increase": [],
        }

    # 计算时间节点
    last_time: datetime = query_post_latest_time(session, search_key.id)

    last_time_1: datetime = last_time - timedelta(hours=1)
    last_time_2: datetime = last_time - timedelta(hours=2)

    # 查询时间范围内的post
    post_list_1: list[int] = query_post_id_by_time_range(session, last_time_1, last_time)
    post_list_2: list[int] = query_post_id_by_time_range(session, last_time_2, last_time_1)

    result = process_word_trend(session, post_list_1, post_list_2)
    session.close()
    return result


def query_word_cloud_trend_by_search_key(keyword: str = Config.SEARCH_KEYWORD) -> dict[str, list[WordFrequencySummary]]:
    """
    通过搜索关键词查询词云数据

    :param keyword:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)

    # 计算时间节点
    last_time: datetime = query_post_latest_time_search_by_keyword(session, keyword)

    last_time_1: datetime = last_time - timedelta(hours=1)
    last_time_2: datetime = last_time - timedelta(hours=2)

    # 查询时间范围内的post
    post_list_1: list[int] = query_post_id_by_time_range_and_keyword(session, keyword, last_time_1, last_time)
    post_list_2: list[int] = query_post_id_by_time_range_and_keyword(session, keyword, last_time_2, last_time_1)

    result = process_word_trend(session, post_list_1, post_list_2)
    session.close()
    return result


def query_word_cloud_hot_trend(keyword: str = Config.SEARCH_KEYWORD) -> dict[datetime, TagTrend]:
    """
    通过搜索关键词查询分时段热度

    :param keyword:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)
    search_key = session.query(SpiderSearchKey).filter(SpiderSearchKey.key == keyword).first()

    if search_key is None:
        FormatLogger.error("Database", "Search key not in database.")
        return {}

    # 计算时间节点
    last_time: datetime = query_post_latest_time(session, search_key.id)

    # Round到整数时间点
    minute = last_time.minute
    last_time = last_time.replace(minute=0, second=0, microsecond=0)
    if minute > 0:
        last_time += timedelta(hours=1)

    result_dict: dict[datetime, TagTrend] = {}
    for index in range(Config.TREND_CYCLE_COUNT):
        last_time_1: datetime = last_time - timedelta(hours=Config.TREND_CYCLE_HOUR * (index + 1))
        last_time_2: datetime = last_time - timedelta(hours=Config.TREND_CYCLE_HOUR * index)

        result_dict[last_time_1] = TagTrend("")
        post_list = query_post_by_time_range(session, last_time_1, last_time_2)

        for item in post_list:
            result_dict[last_time_1].add_post(
                item.user_id, item.attitudes_count, item.comments_count, item.reposts_count, True
            )

    for key, value in result_dict.items():
        value.update_trend()

    session.close()
    return result_dict


def query_word_cloud_hot_trend_by_search_key(keyword: str = Config.SEARCH_KEYWORD) -> dict[datetime, TagTrend]:
    """
    通过搜索关键词查询分时段热度

    :param keyword:
    :return:
    """
    session: scoped_session = db.create_scoped_session(None)

    # 计算时间节点
    last_time: datetime = query_post_latest_time_search_by_keyword(session, keyword)

    # Round到整数时间点
    minute = last_time.minute
    last_time = last_time.replace(minute=0, second=0, microsecond=0)
    if minute > 0:
        last_time += timedelta(hours=1)

    result_dict: dict[datetime, TagTrend] = {}
    for index in range(Config.TREND_CYCLE_COUNT):
        last_time_1: datetime = last_time - timedelta(hours=Config.TREND_CYCLE_HOUR * (index + 1))
        last_time_2: datetime = last_time - timedelta(hours=Config.TREND_CYCLE_HOUR * index)

        result_dict[last_time_1] = TagTrend("")
        post_list = query_post_by_time_range_and_keyword(session, keyword, last_time_1, last_time_2)
        for item in post_list:
            result_dict[last_time_1].add_post(
                item.user_id, item.attitudes_count, item.comments_count, item.reposts_count, True
            )

    for key, value in result_dict.items():
        value.update_trend()

    session.close()
    return result_dict


def process_word_trend(session: scoped_session, post_list_1: list[int],
                       post_list_2: list[int]) -> dict[str, list[WordFrequencySummary]]:
    """
    计算热度变化

    :param session:
    :param post_list_1:
    :param post_list_2:
    :return:
    """
    split_list_1: list[WordSpiltResult] = session.query(WordSpiltResult).filter(
        WordSpiltResult.post_id.in_(post_list_1)
    ).all()
    split_list_2: list[WordSpiltResult] = session.query(WordSpiltResult).filter(
        WordSpiltResult.post_id.in_(post_list_2)
    ).all()

    # 加权结果
    sum_list_1: list[WordFrequencySummary] = sum_word_frequency(split_list_1)
    sum_list_2: list[WordFrequencySummary] = sum_word_frequency(split_list_2)

    # 遍历获取数据
    delta_dict: dict[str, int] = {}
    for item in sum_list_1:
        delta_dict[item.key] = item.count
    for item in sum_list_2:
        if item.key in delta_dict:
            delta_dict[item.key] -= item.count
        else:
            delta_dict[item.key] = -item.count

    # noinspection PyTypeChecker
    sort_result: list[tuple[str, int]] = sorted(delta_dict.items(), key=lambda key_value_pair: key_value_pair[1])

    # 增长列表
    count = 0
    increase_list: list[WordFrequencySummary] = []
    for item in sort_result[::-1]:
        if item[1] <= 0:
            if count < 5:
                continue
            else:
                FormatLogger.warning("Database", "No enough word trend, value maybe null")

        increase_list.append(WordFrequencySummary(item[0], item[1]))
        count += 1

        if count >= 5:
            break

    # 下降列表
    count = 0
    decrease_list: list[WordFrequencySummary] = []
    for item in sort_result:
        if item[1] >= 0:
            if count < 5:
                continue
            else:
                FormatLogger.warning("Database", "No enough word trend, value maybe null")

        decrease_list.append(WordFrequencySummary(item[0], item[1]))
        count += 1

        if count >= 5:
            break

    return {
        "decrease": decrease_list,
        "increase": increase_list
    }


def sum_word_frequency(split_list: list[WordSpiltResult], limit: int = None) -> list[WordFrequencySummary]:
    result_list: dict[str, WordFrequencySummary] = {}
    for spilt in split_list:
        if spilt.key in result_list:
            result_list[spilt.key].add_result(spilt.count, spilt.emotion)
        else:
            result_list[spilt.key] = WordFrequencySummary(spilt.key, spilt.count, spilt.emotion)

    summary_list = [item for key, item in result_list.items()]
    summary_list.sort(key=lambda summary: summary.count, reverse=True)

    if limit is None or len(summary_list) < limit:
        return summary_list

    return summary_list[:limit]


def query_post_search_by_keyword(session: scoped_session, keyword: str) -> list[int]:
    """
    查询搜索关键词

    :param session:
    :param keyword: 搜索关键词
    :return:
    """
    search_list = keyword.split(" ")

    filter_tag_rule = or_(*[SpiderOriginPostData.tags.like("%" + word + "%") for word in search_list])
    filter_content_rule = or_(*[SpiderOriginPostData.content.like("%" + word + "%") for word in search_list])
    result = session.query(SpiderOriginPostData).filter(or_(filter_tag_rule, filter_content_rule)).all()

    search_result_list = [item.id for item in result]
    return search_result_list


def query_post_latest_time(session: scoped_session, search_key_id: str) -> datetime:
    """
    查询最后的post时间

    :param session:
    :param search_key_id: 搜索关键词
    :return:
    """
    result = session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.search_key_id == search_key_id
    ).order_by(SpiderOriginPostData.time.desc()).first()

    return result.time


def query_post_latest_time_search_by_keyword(session: scoped_session, keyword: str) -> datetime:
    """
    查询最后的post时间

    :param session:
    :param keyword: 搜索关键词
    :return:
    """
    search_list = keyword.split(" ")

    filter_tag_rule = or_(*[SpiderOriginPostData.tags.like("%" + word + "%") for word in search_list])
    filter_content_rule = or_(*[SpiderOriginPostData.content.like("%" + word + "%") for word in search_list])
    result = session.query(SpiderOriginPostData).filter(or_(filter_tag_rule, filter_content_rule)).order_by(
        SpiderOriginPostData.tags.desc()
    ).first()

    return result.time


def query_post_id_by_time_range(session: scoped_session, time_start: datetime, time_end: datetime) -> list[int]:
    """
    通过时间范围查询

    :param session:
    :param time_start: 开始时间
    :param time_end: 结束时间
    :return:
    """
    result = session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.time <= time_end, SpiderOriginPostData.time > time_start
    ).all()

    search_result_list = [item.id for item in result]
    return search_result_list


def query_post_id_by_time_range_and_keyword(session: scoped_session, keyword: str,
                                            time_start: datetime, time_end: datetime) -> list[int]:
    """
    通过时间范围和关键词查询

    :param session:
    :param keyword: 搜索关键词
    :param time_start: 开始时间
    :param time_end: 结束时间
    :return:
    """
    search_list = keyword.split(" ")

    filter_tag_rule = or_(*[SpiderOriginPostData.tags.like("%" + word + "%") for word in search_list])
    filter_content_rule = or_(*[SpiderOriginPostData.content.like("%" + word + "%") for word in search_list])

    result = session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.time <= time_end,
        SpiderOriginPostData.time > time_start,
        or_(filter_tag_rule, filter_content_rule)
    ).all()

    search_result_list = [item.id for item in result]
    return search_result_list


def query_post_by_time_range(session: scoped_session, time_start: datetime,
                             time_end: datetime) -> list[SpiderOriginPostData]:
    """
    通过时间范围查询

    :param session:
    :param time_start: 开始时间
    :param time_end: 结束时间
    :return:
    """
    return session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.time <= time_end, SpiderOriginPostData.time > time_start
    ).all()


def query_post_by_time_range_and_keyword(session: scoped_session, keyword: str,
                                         time_start: datetime, time_end: datetime) -> list[SpiderOriginPostData]:
    """
    通过时间范围和关键词查询

    :param session:
    :param keyword: 搜索关键词
    :param time_start: 开始时间
    :param time_end: 结束时间
    :return:
    """
    search_list = keyword.split(" ")

    filter_tag_rule = or_(*[SpiderOriginPostData.tags.like("%" + word + "%") for word in search_list])
    filter_content_rule = or_(*[SpiderOriginPostData.content.like("%" + word + "%") for word in search_list])

    return session.query(SpiderOriginPostData).filter(
        SpiderOriginPostData.time <= time_end,
        SpiderOriginPostData.time > time_start,
        or_(filter_tag_rule, filter_content_rule)
    ).all()
