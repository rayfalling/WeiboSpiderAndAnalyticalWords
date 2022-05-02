# coding: utf-8

# 全局调试开关
import os

# 全局调试开关
from datetime import timedelta

GLOBAL_DEBUG = True

# 线程池最大数量
THREAD_MAX_COUNT = os.cpu_count()

# 单次情感权重
WORD_SENTIMENT_WEIGHT = 0.7

# 中性词权重范围
NEUTRAL_WORD_RANGE = 0.3

# 词条相关微博数量权重
TAG_TREND_POST_COUNT_WEIGHT = 40

# 词条相关发博作者数去重权重
TAG_TREND_POST_AUTHOR_WEIGHT = 15

# 词条相关微博点赞量权重
TAG_TREND_POST_ATTITUDE_WEIGHT = 10

# 词条相关微博转发量权重
TAG_TREND_POST_REPOST_WEIGHT = 15

# 词条相关微博转发量权重
TAG_TREND_POST_COMMENT_WEIGHT = 20


# Flask 项目配置
class AppConfig(object):
    DEBUG = True
    SECRET_KEY = "your_secret_key"

    # 自动Session30分钟过期
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = r"mysql://root:PASSWORD@sh-home.rayfalling.com:3307/GraduationProject?charset=utf8mb4"
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 900,
        "pool_size": 10,
        "max_overflow": 5,
    }
