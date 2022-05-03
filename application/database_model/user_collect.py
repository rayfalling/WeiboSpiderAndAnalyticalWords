from ..core import db

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER

__all__ = ("UserCollect",)


class UserCollect(db.Model):
    """
    用户收藏表

    用于储存用户收藏数据
    """
    __table_name__ = "user_info"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 用户ID 外键
    user_id = db.Column(INTEGER, ForeignKey("user_info.id"))
    # 资讯Id 外键
    post_id = db.Column(INTEGER, ForeignKey("spider_origin_post_data.id"))

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
