import typing

from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import WordSpiltResult

from libs import FormatLogger
from libs.data_model import WordFrequency

__all__ = ("insert_all_word_split_data",)


def insert_all_word_split_data(word_spilt_list: typing.List[WordFrequency]):
    """
    将分词结果写入数据库
    全量查询一次数据库, 获取当前数据库内容副本, 再次去重

    :param word_spilt_list: 爬虫获取的数据结果
    :return:
    """

    if len(word_spilt_list) == 0:
        return 0

    search_key_id = word_spilt_list[0].search_key_id

    session: scoped_session = db.create_scoped_session(None)
    database_split_data: list[WordSpiltResult] = query_all_spilt_result(session, search_key_id)

    words: list[str] = [item.key for item in database_split_data]

    for item in word_spilt_list:
        if item.key in words:
            find_data = next((data for data in database_split_data if data.key == item.key), None)

            if None is find_data:
                FormatLogger.error("Database", "Split word modified while process database")
                session.delete(item)

            find_data.count = item.count
        else:
            origin_data = WordSpiltResult(item)
            session.add(origin_data)

    session.commit()
    session.close()


def query_all_spilt_result(session: scoped_session, search_key_id: int) -> list[WordSpiltResult]:
    """
    获取当前所有已存在的分词结果

    :return:
    """
    return session.query(WordSpiltResult).filter(WordSpiltResult.search_key_id == search_key_id).all()
