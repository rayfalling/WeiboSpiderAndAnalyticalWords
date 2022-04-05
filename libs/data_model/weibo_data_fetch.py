# coding: utf-8
import typing

from json import JSONEncoder
from datetime import datetime, time


class CommentData(object):
    """
    评论回复数据
    """

    def __init__(self, count: int, comments: typing.Optional[typing.List[str]] = None):
        """

        :param count: 评论数
        :param comments: 评论回复
        """
        if comments is None:
            comments = []

        self.count: int = count
        self.comment: typing.Optional[typing.List[str]] = comments

    def get_comment_count(self) -> int:
        """
        获取有效评论数量

        :return: 有效评论数
        """
        return len(self.comment)


class PostData(object):
    """
    爬虫数据基类
    """

    def __init__(self, mid: int = -1, user_id: int = -1, username: str = "", content: str = "",
                 post_time: datetime = datetime.now(), attitudes_count: int = 0, comments_count: int = 0,
                 reposts_count: int = 0):
        """
        微博数据构造函数

        :param mid: 资讯Id
        :param user_id: 用户Id
        :param username: 用户名
        :param content: 微博内容
        :param post_time: 微博发布时间
        :param attitudes_count: 点赞量
        :param comments_count: 评论量
        :param reposts_count: 转发量
        """

        # 资讯Id
        self.mid: int = mid
        # 用户Id
        self.user_id: int = user_id
        # 微博内容
        self.content: str = content
        # 用户名
        self.username: str = username

        # 微博发布时间
        self.time: datetime = post_time

        # 转发量
        self.reposts_count: int = reposts_count
        # 点赞量
        self.attitudes_count: int = attitudes_count
        # 评论数据
        self.comment: CommentData = CommentData(comments_count)

        self.__post_origin_url = ""

    def set_content(self, content: str):
        """
        更新全文内容

        :param content: 微博帖子内容
        :return: None
        """
        self.content = content

    def set_scheme(self, scheme: str):
        """
        设置微博数据原始页面, 用于获取和更新评论相关

        :param scheme: 原始地址
        :return:
        """
        self.__post_origin_url = scheme

    def get_scheme(self) -> str:
        """
        获取原始页面地址

        :return: 页面地址
        """
        return self.__post_origin_url


class PostDataEncoder(JSONEncoder):
    def default(self, obj: PostData):
        return {
            "data": {
                "mid": obj.mid,
                "time": obj.time.strftime("%Y-%m-%d %H:%M:%S"),
                "text": obj.content,
                "userid": obj.user_id,
                "username": obj.username,
                "reposts_count": obj.reposts_count,
                "attitudes_count": obj.attitudes_count,

                "comment":{
                    "comments_count": obj.comment.count,
                    "comments_list": obj.comment.comment,
                }
            },
            "scheme": obj.get_scheme()
        }
