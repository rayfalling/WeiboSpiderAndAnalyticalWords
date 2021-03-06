from datetime import datetime

from ..core import db

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import INTEGER, DATETIME

__all__ = ("UserHistory",)


class UserHistory(db.Model):
    """
    用户浏览历史表

    用于储存用户浏览历史数据
    """
    __table_name__ = "user_info"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    # 全局ID 自增
    id = db.Column(INTEGER, index=True, primary_key=True, autoincrement=True, nullable=False)
    # 用户ID 外键
    user_id = db.Column(INTEGER, ForeignKey("user_info.id"))
    # 资讯Id 外键
    post_id = db.Column(INTEGER, ForeignKey("spider_origin_post_data.id"))
    # 浏览时间
    time = db.Column(DATETIME, nullable=False)

    def __init__(self, user_id, post_id, time: datetime = datetime.now()):
        self.user_id = user_id
        self.post_id = post_id
        self.time = time.strftime("%Y-%m-%d %H:%M:%S")

    def update_time(self):
        """
        更新浏览时间

        :return:
        """
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
