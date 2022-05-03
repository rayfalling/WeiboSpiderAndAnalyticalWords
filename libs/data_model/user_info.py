# coding: utf-8
from datetime import datetime


class UserData(object):
    """
    用户数据
    """

    def __init__(self, username: str, nickname: str, avatar: str, user_type: int):
        """

        :param username: 用户ID 手机号
        :param nickname: 用户名 昵称
        :param avatar: 用户头像
        :param user_type: 用户类型 0 为管理员 1 为普通用户
        """

        self.avatar = avatar
        self.username = username
        self.nickname = nickname
        self.user_type = user_type

    def __repr__(self):
        return str({
            "avatar": self.avatar,
            "nickname": self.nickname,
            "username": self.username,
            "user_type": self.user_type
        })


class UserActivity(object):
    """
    搜索结果
    """

    def __init__(self, post_id: int, tags: str, content: str, time: datetime, activity_time: datetime = None):
        """

        :param post_id: 微博数据库存储Id
        :param tags: 微博标签数据
        :param time: 微博发布时间
        :param activity_time: 活动时间
        :param content: 微博内容
        """

        self.tags = tags
        self.time = time
        self.post_id = post_id
        self.content = content
        self.activity_time = activity_time

    def __repr__(self):
        return str({
            "tags": self.tags,
            "time": self.time.strftime("%Y-%m-%d %H:%M:%S"),
            "post_id": self.post_id,
            "content": self.content
        })
