from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderOriginPostData, SpiderOriginCommentData, UserHistory, UserCollect, WordSpiltResult

from libs import FormatLogger

__all__ = ("clear_all_data",)


def clear_all_data():
    """
    清除所有旧数据

    :return:
    """
    FormatLogger.info("Database", "Starting clear all old data...")
    session: scoped_session = db.create_scoped_session(None)

    # clean history
    clean_table_data(session, UserHistory)

    # clean collect
    clean_table_data(session, UserCollect)

    # clean word split result
    clean_table_data(session, WordSpiltResult)

    # clean comment
    clean_table_data(session, SpiderOriginCommentData)

    # clean post
    clean_table_data(session, SpiderOriginPostData)
    session.close()


def clean_table_data(session: scoped_session, table):
    """
    清空表数据

    :param session:
    :param table:
    :return:
    """
    data_list = session.query(table).all()
    for data in data_list:
        session.delete(data)
    session.commit()

