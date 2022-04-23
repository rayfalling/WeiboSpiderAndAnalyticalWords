# coding: utf-8

# 全局调试开关
import os

# 全局调试开关
GLOBAL_DEBUG = True

# jieba分词多线程加速
MULTI_PROCESS_JIEBA = False

# 线程池最大数量
THREAD_MAX_COUNT = os.cpu_count()


# Flask 项目配置
class AppConfig(object):
    DEBUG = True
    SECRET_KEY = "your_secret_key"
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
