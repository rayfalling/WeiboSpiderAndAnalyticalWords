# coding=utf-8
import sys
import logging
import logging.handlers

from datetime import datetime
from utils import get_temp_dir
from config.flask_config import GLOBAL_DEBUG

ENABLE_DEBUG = GLOBAL_DEBUG


class ColorFormatter(logging.Formatter):
    warning = "\033[33m"
    error = "\033[31;1m"
    info = "\033[34m"
    debug = "\033[36m"
    reset = "\033[0m"

    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)
        self.FORMATS = {
            logging.INFO: logging.Formatter(self.info + self._fmt + self.reset),
            logging.DEBUG: logging.Formatter(self.debug + self._fmt + self.reset),
            logging.ERROR: logging.Formatter(self.error + self._fmt + self.reset),
            logging.WARNING: logging.Formatter(self.warning + self._fmt + self.reset),
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        return log_fmt.format(record)


rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

fileHandler = logging.handlers.TimedRotatingFileHandler(
    get_temp_dir() + "/logs/log.txt", backupCount=10, when="H", interval=6, encoding="utf-8"
)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logging.Formatter("%(message)s"))
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG if ENABLE_DEBUG else logging.INFO)
consoleHandler.setFormatter(ColorFormatter("%(message)s"))
rootLogger.addHandler(consoleHandler)

# Hack for request logging settings
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.WARNING)

# Hack for Pillow logging settings
pillow_log = logging.getLogger("PIL.Image")
pillow_log.setLevel(logging.WARNING)

# Hack for jieba logging settings
jieba_log = logging.getLogger("jieba")
jieba_log.setLevel(logging.WARNING)
# Remove jieba defined handler
jieba_log.handlers.clear()


def format_message(source: str, log_type: str, message: str):
    """
    格式化输出

    @param source: 来源
    @param log_type: 日志类型
    @param message: 消息内容
    @return:
    """
    current_time = "[{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3])
    log_type_str = "[{:^8}]".format(log_type)
    source_str = "[{}]".format(source)
    output = [current_time, log_type_str, source_str, message]
    return " ".join([str(i) for i in output])


class FormatLogger(object):
    @staticmethod
    def warning(source: str, message: str):
        logging.warning(format_message(source, "WARNING", message))

    @staticmethod
    def error(source: str, message: str):
        logging.error(format_message(source, "ERROR", message))

    @staticmethod
    def info(source: str, message: str):
        logging.info(format_message(source, "INFO", message))

    @staticmethod
    def debug(source: str, message: str):
        if ENABLE_DEBUG:
            logging.debug(format_message(source, "DEBUG", message))
