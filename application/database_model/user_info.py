from ..core import db

from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

__all__ = ("UserInfo",)


class UserInfo(db.Model):
    """
    用户信息表

    用于储存用户数据
    """
    __table_name__ = "user_info"

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 用户ID 手机号
    user_id = db.Column(VARCHAR(11), nullable=False)
    # 用户名 昵称
    username = db.Column(VARCHAR(64), nullable=False)
    # 用户密码
    password = db.Column(VARCHAR(64), nullable=False)
    # 用户头像
    avatar = db.Column(VARCHAR(256), nullable=False)
    # 用户类型 0 为管理员 1 为普通用户
    user_type = db.Column(INTEGER, nullable=False, default=1)

    def __init__(self, user_id, username, password, avatar, user_type):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.avatar = avatar
        self.user_type = user_type
