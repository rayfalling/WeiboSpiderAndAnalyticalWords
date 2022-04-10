# coding: utf-8

# 全局调试开关
GLOBAL_DEBUG = True


# Flask 项目配置
class AppConfig(object):
    DEBUG = True
    SECRET_KEY = 'your_secret_key'
    SCHEDULER_API_ENABLED = True
