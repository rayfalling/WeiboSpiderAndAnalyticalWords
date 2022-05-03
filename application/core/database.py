from flask_sqlalchemy import SQLAlchemy
from pymysql import install_as_MySQLdb

from .core import app

__all__ = ("db",)

# install MySQLdb
install_as_MySQLdb()

db = SQLAlchemy(app)
