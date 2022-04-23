from ..core import db

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, BIGINT, NVARCHAR, INTEGER, DATETIME

from libs.data_model import PostData

__all__ = ("SpiderOriginPostData",)


class SpiderOriginPostData(db.Model):
    """
    原始数据表

    用于储存原始爬虫数据
    """
    __table_name__ = "spider_origin_post_data"

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 微博Id
    mid = db.Column(BIGINT, nullable=False)
    # 微博用户ID
    user_id = db.Column(BIGINT, nullable=False)
    # 微博用户名称
    username = db.Column(NVARCHAR(64), nullable=False)
    # 微博Tags
    tags = db.Column(NVARCHAR(256), nullable=False)
    # 微博文本数据
    content = db.Column(LONGTEXT, nullable=False)
    # 搜索关键词外键
    search_key_id = db.Column(INTEGER, ForeignKey("spider_origin_post_data.id"))
    # 发布时间
    time = db.Column(DATETIME, nullable=False)
    # 点赞量
    attitudes_count = db.Column(INTEGER, nullable=False, default=0)
    # 评论量
    comments_count = db.Column(INTEGER, nullable=False, default=0)
    # 转发量
    reposts_count = db.Column(INTEGER, nullable=False, default=0)

    def __init__(self, post_data: PostData, search_key_id: int):
        self.mid = post_data.mid
        self.user_id = post_data.user_id
        self.username = post_data.username
        self.tags = "#".join(post_data.tags)
        self.content = post_data.content
        self.search_key_id = search_key_id
        self.time = post_data.time.strftime("%Y-%m-%d %H:%M:%S")
        self.attitudes_count = post_data.attitudes_count
        self.comments_count = post_data.comment.count
        self.reposts_count = post_data.reposts_count
