from flask import Flask

from config.flask_config import AppConfig

# core app config here
app = Flask(__name__)

app.config.from_object(AppConfig)

__all__ = ("app",)
