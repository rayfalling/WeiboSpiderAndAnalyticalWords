# coding: utf-8
import re

__all__ = ("clean_text",)

tag_regex = re.compile(r"#[^#]+#", re.S)
user_regex = re.compile(r"@[^ ]+ ", re.S)
html_regex = re.compile(r"(<)[^>]+>", re.S)


def clean_text(text):
    """
    清除文本中的标签等信息
    """

    text = tag_regex.sub("", text)
    text = html_regex.sub("", text)
    text = user_regex.sub("", text)
    return text.strip()
