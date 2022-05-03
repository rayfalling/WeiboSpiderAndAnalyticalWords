from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import UserCollect, UserHistory
from ..database_model import SpiderOriginPostData, SpiderOriginCommentData, WordSpiltResult, SpiderSearchKey

from libs import FormatLogger

__all__ = ("delete_post_with_id", "delete_comment_with_id", )


# noinspection DuplicatedCode
def delete_post_with_id(post_id: int) -> bool:
    """
    获取当前所有的评论数据

    :return:
    """
    FormatLogger.info("Database", "Deleting post id {}".format(post_id))
    session: scoped_session = db.create_scoped_session(None)

    # 删除收藏数据
    collect_result = session.query(UserCollect).filter(UserCollect.post_id == post_id).all()
    for collect in collect_result:
        session.delete(collect)
    session.commit()

    # 删除分词结果
    history_result = session.query(UserHistory).filter(UserHistory.post_id == post_id).all()
    for history in history_result:
        session.delete(history)
    session.commit()

    # 删除分词结果
    split_result = session.query(WordSpiltResult).filter(WordSpiltResult.post_id == post_id).all()
    for split in split_result:
        session.delete(split)
    session.commit()

    # 删除评论结果
    comment_result = session.query(SpiderOriginCommentData).filter(SpiderOriginCommentData.post_id == post_id).all()
    for comment in comment_result:
        session.delete(comment)
    session.commit()

    post = session.query(SpiderOriginPostData).filter(SpiderOriginPostData.id == post_id).first()

    if post is None:
        return False

    session.delete(post)
    session.commit()
    session.close()
    return True


# noinspection DuplicatedCode
def delete_comment_with_id(post_id: int, comment_id: int) -> tuple[bool, int]:
    """
    获取当前所有的评论数据

    :return:
    """
    FormatLogger.info("Database", "Deleting post id {}".format(post_id))
    session: scoped_session = db.create_scoped_session(None)

    # 删除分词结果
    split_result = session.query(WordSpiltResult).filter(WordSpiltResult.post_id == post_id).all()
    for split in split_result:
        session.delete(split)
    session.commit()

    post = session.query(SpiderOriginPostData).filter(SpiderOriginPostData.id == post_id).first()
    search = session.query(SpiderSearchKey).filter(SpiderSearchKey.id == post.search_key_id).first()
    comment = session.query(SpiderOriginCommentData).filter(SpiderOriginCommentData.id == comment_id).first()
    if post is None or comment is None or search is None:
        return False, -1

    search_key = search.key

    # 删除评论结果
    session.delete(comment)
    session.commit()
    session.close()

    return True, search_key
