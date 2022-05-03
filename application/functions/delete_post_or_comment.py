from sqlalchemy.orm import scoped_session

from ..core import db
from ..database_model import SpiderOriginPostData, SpiderOriginCommentData, WordSpiltResult

from libs import FormatLogger

__all__ = ("delete_post_with_id",)


def delete_post_with_id(post_id: int) -> bool:
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


def delete_comment_with_id(post_id: int) -> bool:
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
