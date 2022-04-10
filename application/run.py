from flask import Flask

from .core import app
from .router import admin_router

__all__ = ("main",)


def init(flask_app: Flask):
    flask_app.register_blueprint(admin_router)


# 主启动函数
def main():
    init(app)
    app.run()
