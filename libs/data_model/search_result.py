# coding: utf-8
from datetime import datetime


class SearchResult(object):
    """
    搜索结果
    """

    def __init__(self, post_id: int, tags: str, content: str, time: datetime):
        """

        :param post_id: 微博数据库存储Id
        :param tags: 微博标签数据
        :param content: 微博内容
        """

        self.tags = tags
        self.time = time
        self.post_id = post_id
        self.content = content

    def __repr__(self):
        return str({
            "tags": self.tags,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "post_id": self.post_id,
            "content": self.content
        })


class PostDetail(object):
    """
    搜索结果
    """

    def __init__(self, post_id: int, username: str = "", tags: str = "", content: str = "",
                 time: datetime = datetime.now(), count: tuple[int, int, int] = (0, 0, 0), comments=None):
        """

        :param post_id: 微博数据库存储Id
        :param username: 微博数据库存储Id
        :param tags: 微博标签数据
        :param content: 微博内容
        :param time: 发布时间
        :param count: 点赞量，评论量，转发量 三元组
        :param comments: 评论列表
        """
        if comments is None:
            comments = []

        # 全局ID 自增
        self.post_id = post_id
        # 微博用户名称
        self.username = username
        # 微博Tags
        self.tags = tags
        # 微博文本数据
        self.content = content
        # 发布时间
        self.time = time
        # 点赞量
        self.attitudes_count = count[0]
        # 评论量
        self.comments_count = count[1]
        # 转发量
        self.reposts_count = count[2]
        # 评论数据
        self.comments = comments

    def __repr__(self):
        return str({
            "tags": self.tags,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "post_id": self.post_id,
            "content": self.content,

            "username": self.username,
            "comments": self.comments,
            "reposts_count": self.reposts_count,
            "comments_count": self.comments_count,
            "attitudes_count": self.attitudes_count,
        })
