from flask import Flask
from flask.logging import default_handler

from config.flask_config import AppConfig
from libs.logger.logging import consoleHandler, fileHandler


# core app config here
app = Flask(__name__)
app.config.from_object(AppConfig)

app.logger.removeHandler(default_handler)

app.logger.addHandler(fileHandler)
app.logger.addHandler(consoleHandler)

__all__ = ("app",)
