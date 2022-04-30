# coding: utf-8


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
