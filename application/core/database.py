from flask_sqlalchemy import SQLAlchemy
from pymysql import install_as_MySQLdb

from .core import app

# install MySQLdb
install_as_MySQLdb()

db = SQLAlchemy(app)
