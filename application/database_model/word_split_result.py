from ..core import db

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import NVARCHAR, INTEGER, FLOAT

from libs.data_model import WordFrequency

__all__ = ("WordSpiltResult",)


class WordSpiltResult(db.Model):
    """
    搜索关键词表

    用于储存搜索过的关键词，处理分词数据
    """
    __table_name__ = "word_split_result"

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 搜索关键词外键
    search_key_id = db.Column(INTEGER, ForeignKey("spider_search_key.id"))
    # 微博数据库Id
    post_id = db.Column(INTEGER, ForeignKey("spider_origin_post_data.id"))
    # 关键词
    key = db.Column(NVARCHAR(256), nullable=False)
    # 词频
    count = db.Column(INTEGER, nullable=False)
    # 情感倾向
    emotion = db.Column(FLOAT, nullable=False)

    def __init__(self, word: WordFrequency):
        self.search_key_id = word.search_key_id
        self.post_id = word.post_id
        self.key = word.key
        self.count = word.count
        self.emotion = word.emotion
