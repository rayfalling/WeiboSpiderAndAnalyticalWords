# coding: utf-8
import re
import html

__all__ = ("split_tags",)


def split_tags(tags: str):
    """
    清除文本中的标签等信息
    """

    tags = tags.split("#")
    if tags[0] == "":
        tags_str = ""
    else:
        tags_str = "".join(["#" + item + "# " for item in tags])

    return tags_str
