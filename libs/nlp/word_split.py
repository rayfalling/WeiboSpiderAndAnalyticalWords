# 分词模块
import os.path
from collections import Counter

import paddle

import jieba
import jieba.posseg

from libs.logger import FormatLogger
from utils import get_project_path

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


__all__ = ("load_jieba_env", "word_split",)


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

    word_list: list[str] = []

    segments = jieba.posseg.cut(delete_punt(origin_string), use_paddle=True, HMM=True)
    for segment, flag in segments:
        if flag in __switch_flags and not __switch_flags[flag]:
            word_list.append(segment)
        elif segment not in STOPWORDS:
            word_list.append(segment)

    return count_word_frequency(word_list)


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


def count_word_frequency(origin_words: list[str]) -> dict:
    """
    获取分词后的词频统计

    :param origin_words:
    :return:
    """
    return dict(Counter(origin_words))
