from ..core import db

from sqlalchemy.dialects.mysql import NVARCHAR, INTEGER

__all__ = ("SpiderSearchKey",)


class SpiderSearchKey(db.Model):
    """
    搜索关键词表

    用于储存搜索过的关键词，处理分词数据
    """
    __table_name__ = "spider_search_key"

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 搜索关键词
    key = db.Column(NVARCHAR(256), nullable=False)

    def __init__(self, key):
        self.key = key
