from ..core import db

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, BIGINT, INTEGER

__all__ = ("SpiderOriginCommentData",)


class SpiderOriginCommentData(db.Model):
    """
    原始数据表

    用于储存原始爬虫数据
    """
    __table_name__ = "spider_origin_comment_data"

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 微博数据库Id
    post_id = db.Column(INTEGER, ForeignKey("spider_origin_post_data.id"))
    # 评论原始Id
    comment_id = db.Column(BIGINT, nullable=False)
    # 评论文本数据
    content = db.Column(LONGTEXT, nullable=False)

    def __init__(self, post_id: int, comment_id: int, comment: str):
        self.post_id = post_id
        self.content = comment
        self.comment_id = comment_id
