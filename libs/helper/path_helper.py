# coding: utf-8

import os


def get_project_path() -> str:
    """
    获取当前项目目录

    :return: 项目路径
    """
    return os.path.join(os.path.dirname(__file__), "../..")


def get_temp_dir() -> str:
    """
    获取临时目录

    :return:
    """
    return os.path.join(get_project_path(), "temp")
