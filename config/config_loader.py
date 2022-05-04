# coding: utf-8
import os

import json


class Config(object):
    # 固定搜索的关键词
    SEARCH_KEYWORD = "鸿星尔克"

    # 单次情感权重
    WORD_SENTIMENT_WEIGHT = 0.7

    # 中性词权重范围
    NEUTRAL_WORD_RANGE = 0.3

    # 词条相关微博数量权重
    TAG_TREND_POST_COUNT_WEIGHT = 40

    # 词条相关发博作者数去重权重
    TAG_TREND_POST_AUTHOR_WEIGHT = 15

    # 词条相关微博点赞量权重
    TAG_TREND_POST_ATTITUDE_WEIGHT = 10

    # 词条相关微博转发量权重
    TAG_TREND_POST_REPOST_WEIGHT = 15

    # 词条相关微博转发量权重
    TAG_TREND_POST_COMMENT_WEIGHT = 20

    @classmethod
    def load(cls):
        from utils import get_project_path
        path = os.path.join(get_project_path(), "data/config.json")

        if not os.path.exists(path):
            from libs import FormatLogger
            FormatLogger.warning("ConfigLoader", "No config file exists")
            return

        with open(path, encoding="utf-8", mode="r") as file:
            result = json.load(file)

            for item in cls.__dict__:
                if item.startswith("__") or item.startswith("_"):
                    continue
                elif callable(getattr(cls, item)):
                    continue
                else:
                    save_name = item.lower()
                    if save_name in result:
                        setattr(cls, item, result[save_name])

    @classmethod
    def save(cls):
        from utils import get_project_path
        path = os.path.join(get_project_path(), "data/config.json")

        with open(path, encoding="utf-8", mode="w") as file:
            result = {}

            for item in cls.__dict__:
                if item.startswith("__") or item.startswith("_"):
                    continue
                elif callable(getattr(cls, item)):
                    continue
                else:
                    save_name = item.lower()
                    result[save_name] = getattr(cls, item)

            json.dump(result, file, ensure_ascii=False, indent=4)
