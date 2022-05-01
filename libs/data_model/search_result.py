# coding: utf-8
from datetime import datetime


class SearchResult(object):
    """
    搜索结果
    """

    def __init__(self, post_id: int, tags: list[str], content: str, time: datetime):
        """

        :param post_id: 微博数据库存储Id
        :param tags: 微博标签数据
        :param content: 微博内容
        """

        self.tags = tags
        self.time = time
        self.post_id = post_id
        self.content = content

