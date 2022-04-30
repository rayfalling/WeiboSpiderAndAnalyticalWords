# 分词模块
import os.path
from collections import Counter

import paddle

import jieba
import jieba.posseg
from snownlp import SnowNLP

from utils import get_project_path
from libs.logger import FormatLogger
from config.flask_config import WORD_SENTIMENT_WEIGHT, NEUTRAL_WORD_RANGE

# 停用词表
STOPWORDS: list[str] = []

WORD_DICT_PATH = "data/dict.txt"
STOPWORD_DICT_PATH = "data/stopword.txt"

ENV_INIT = False


def load_jieba_env():
    global STOPWORDS, ENV_INIT

    if ENV_INIT:
        return

    FormatLogger.info("SplitWord", "loading jieba libs and dicts...")
    jieba.set_dictionary(os.path.join(get_project_path(), WORD_DICT_PATH))

    # 删除多余的logger
    import logging
    jieba.default_logger.handlers.clear()
    jieba.default_logger.setLevel(logging.WARNING)

    paddle.enable_static()
    jieba.initialize()
    jieba.enable_paddle()

    with open(os.path.join(get_project_path(), STOPWORD_DICT_PATH), mode="r", encoding="utf-8") as fr:
        lines = fr.readlines()
        STOPWORDS = [item.strip() for item in lines]

    ENV_INIT = True


__all__ = ("load_jieba_env", "word_split", "map_sentiment_to_int_emotion", )


def word_split(origin_string: str, drop_conjunction: bool = True, drop_particle: bool = True,
               drop_adverb: bool = True, drop_pronoun: bool = True, drop_preposition: bool = True) -> dict:
    """
    调用分词系统完成分词

    :param origin_string: 原始句子
    :param drop_conjunction: 是否抛弃连词
    :param drop_particle: 是否抛弃助词
    :param drop_adverb: 是否抛弃副词
    :param drop_pronoun: 是否抛弃代词
    :param drop_preposition: 是否抛弃介词
    :return:
    """

    __switch_flags = {
        # 连词
        "c": drop_conjunction,
        # 助词
        "u": drop_particle,
        # 副词
        "d": drop_adverb,
        # 代词
        "r": drop_pronoun,
        # 介词
        "p": drop_preposition,
        # 标点符号
        "w": True,
    }

    word_list: list[tuple[str, float]] = []

    processed_origin_str = delete_punt(origin_string)
    if origin_string == "":
        return {}

    processed_origin_sentiment = remap_sentiment_range(SnowNLP(origin_string).sentiments)

    segments = jieba.posseg.cut(processed_origin_str, use_paddle=True, HMM=True)
    for segment, flag in segments:
        if segment.strip() == "":
            continue

        if flag in __switch_flags:
            if not __switch_flags[flag]:
                sen = remap_sentiment_range(SnowNLP(segment).sentiments)
                word_list.append(
                    (segment, merge_sentiment_range(sentiment_string=processed_origin_sentiment, sentiment_word=sen))
                )
            else:
                continue
        elif segment not in STOPWORDS:
            sen = remap_sentiment_range(SnowNLP(segment).sentiments)
            word_list.append(
                (segment, merge_sentiment_range(sentiment_string=processed_origin_sentiment, sentiment_word=sen))
            )

    final_data = {}
    count_data = count_word_frequency(word_list)
    for key, value in count_data.items():
        final_data[key[0]] = (value, key[1])

    return final_data


# 中文标点符号集
asterism = set(
    u'''
    :!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），
    ．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《
    「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…
    '''
)


def delete_punt(origin_string: str):
    """
    预处理中文标点符号

    :param origin_string: 原始句子
    :return:
    """
    return ''.join(filter(lambda x: x not in asterism, origin_string))


def count_word_frequency(origin_words: list[tuple[str, float]]) -> dict:
    """
    获取分词后的词频统计

    :param origin_words:
    :return:
    """
    return dict(Counter(origin_words))


def remap_sentiment_range(sentiment: float) -> float:
    """
    重映射情感数值范围

    :param sentiment:
    :return:
    """
    return round(sentiment * 2 - 1, 4)


def merge_sentiment_range(sentiment_string: float, sentiment_word: float) -> float:
    """
    合并句子情感权重和词语情感权重

    :param sentiment_string: 句子情感权重
    :param sentiment_word: 词语情感权重
    :return:
    """
    return round(sentiment_word * WORD_SENTIMENT_WEIGHT + sentiment_string * (1.0 - WORD_SENTIMENT_WEIGHT), 4)


def map_sentiment_to_int_emotion(sentiment: float) -> int:
    """
    获取词语情感程度

    :param sentiment:
    :return:
    """
    if sentiment < -NEUTRAL_WORD_RANGE:
        return -1
    elif sentiment > NEUTRAL_WORD_RANGE:
        return 1

    return 0
