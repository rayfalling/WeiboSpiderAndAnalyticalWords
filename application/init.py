import atexit

from flask import Flask

from config import Config, GLOBAL_DEBUG
from .core import app, db, CustomRequestHandler
from .router import user_router, admin_router, search_router, detail_router, word_cloud_router, user_activity_router

__all__ = ("main",)


# noinspection PyUnresolvedReferences
def init_database():
    from libs import FormatLogger
    import application.database_model

    db.create_all()
    FormatLogger.info("Database", "Creating Database tables success.")


def init(flask_app: Flask):
    flask_app.register_blueprint(user_router)
    flask_app.register_blueprint(admin_router)
    flask_app.register_blueprint(search_router)
    flask_app.register_blueprint(detail_router)
    flask_app.register_blueprint(word_cloud_router)
    flask_app.register_blueprint(user_activity_router)


def load_config():
    from libs import FormatLogger
    FormatLogger.info("App", "Loading application config.")
    Config.load()


def save_config():
    from libs import FormatLogger
    FormatLogger.info("App", "Saving application config.")
    Config.save()


# 主启动函数
def main():
    # Load Config
    load_config()
    atexit.register(save_config)

    # 注册路由时间
    init(app)
    # 创建数据库相关
    init_database()
    # 启动Flask
    app.run("0.0.0.0", port=8088, debug=GLOBAL_DEBUG, threaded=True, request_handler=CustomRequestHandler)
