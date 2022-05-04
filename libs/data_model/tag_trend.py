# coding: utf-8
from config import Config


class TagTrend(object):
    """
    搜索结果
    """

    def __init__(self, tag: str):
        """

        :param tag: 标签名称
        """
        # 标签名称
        self.tag: str = tag

        # 微博数量计算
        self.__post_count: int = 0

        # 微博作者数量统计
        self.__post_author_set = set()

        # 热度指数
        self.__trend: float = 0

        # 总转发数
        self.__reposts: int = 0
        # 总评论数
        self.__comments: int = 0
        # 总点赞数
        self.__attitudes: int = 0

        # 热度数据是否被刷新
        self.__dirty: bool = True

    def get_trend(self):
        """
        获取计算热度值

        :return:
        """
        if self.__dirty:
            self.update_trend()

        return self.__trend

    def add_post(self, author_id: int, attitude: int, comment: int, repost: int, update_trend: bool = False):
        """
        记录微博数据，计算热度

        :param author_id: 微博作者
        :param attitude: 点赞数
        :param comment: 评论数
        :param repost: 转发数

        :param update_trend: 是否立即更新热度预测值
        :return:
        """
        self.__post_count += 1
        self.__post_author_set.add(author_id)

        self.__reposts += repost
        self.__comments += comment
        self.__attitudes += attitude

        self.__dirty = True
        if update_trend:
            self.update_trend()

    def update_trend(self):
        """
        更新热度计算值

        :return:
        """

        if not self.__dirty:
            return

        self.__trend = self.__post_count * Config.TAG_TREND_POST_COUNT_WEIGHT

        self.__trend += self.__reposts * Config.TAG_TREND_POST_REPOST_WEIGHT
        self.__trend += self.__comments * Config.TAG_TREND_POST_COMMENT_WEIGHT
        self.__trend += self.__attitudes * Config.TAG_TREND_POST_ATTITUDE_WEIGHT

        self.__trend += len(self.__post_author_set) * Config.TAG_TREND_POST_AUTHOR_WEIGHT

        self.__dirty = False

    def __repr__(self):
        return str({
            "tag": self.tag,
            "reposts": self.__reposts,
            "comments": self.__comments,
            "attitudes": self.__attitudes,
            "post_count": self.__post_count,
        })
