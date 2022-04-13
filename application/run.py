from flask import Flask

from .core import app, db
from .router import admin_router

from config.flask_config import GLOBAL_DEBUG

__all__ = ("main",)


# noinspection PyUnresolvedReferences
def init_database():
    from libs import FormatLogger
    import application.database_model

    db.create_all()
    FormatLogger.info("Database", "Creating Database tables success.")


def init(flask_app: Flask):
    flask_app.register_blueprint(admin_router)


# 主启动函数
def main():
    # 注册路由时间
    init(app)
    # 创建数据库相关
    init_database()
    # 启动Flask
    app.run("0.0.0.0", port=8080, debug=GLOBAL_DEBUG)
