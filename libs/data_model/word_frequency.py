# coding: utf-8

class PostDataContent(object):
    """
    分词数据类
    """

    def __init__(self, post_id: int, content: str, comments: list[str]):
        self.id = post_id
        self.content = content
        self.comments: list[str] = comments

    def __repr__(self):
        return str({
            "id": self.id,
            "content": self.content,
            "comments": self.comments
        })


class WordFrequency(object):
    """
    爬虫数据基类
    """

    def __init__(self, search_key_id: int, key: str, count: int = 0, emotion: int = 0):
        """
        微博数据构造函数

        :param search_key_id: 搜索关键词Id
        :param key: 关键词
        :param count: 词频
        :param emotion: 情感倾向
        """

        # 搜索关键词Id
        self.search_key_id: int = search_key_id
        # 关键词
        self.key: str = key

        # 词频
        self.count: int = count
        # 情感倾向
        self.emotion: int = emotion

    def __repr__(self):
        return str({
            "search_key_id": self.search_key_id,
            "key": self.key,
            "count": self.count,
            "emotion": self.emotion
        })
