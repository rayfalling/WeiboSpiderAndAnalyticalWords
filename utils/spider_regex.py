# coding: utf-8
import re
import html

__all__ = ("clean_text",)

# 标签
tag_regex = re.compile(r"#[^#]+#", re.UNICODE)
# html页签数据
html_regex = re.compile(r"(<)[^>]+>", re.UNICODE)

# 转发
repost_regex = re.compile(r"//[\s]?:", re.UNICODE)
# 评论
comment_regex = re.compile(r"回复:", re.UNICODE)

# 单独@用户
at_user_regex = re.compile(r"<a href=[\"\'][\s\S]*?[\"\']>@[^<]*?</a>", re.UNICODE)
# 链接
url_regex = re.compile(r"<span class=[\"\']surl-text[\"\']>[\s\S]*?</span>", re.UNICODE)


def clean_text(text):
    """
    清除文本中的标签等信息
    """

    text = html.unescape(text)

    # 提取tag
    tags = tag_regex.findall(text)

    # 移除所有tag
    text = tag_regex.sub("", text)

    # 提取链接内容
    links = url_regex.findall(text)

    # 移除所有链接内容
    text = url_regex.sub("", text)

    # 预处理@信息
    text = at_user_regex.sub("", text)

    # 处理html标签信息
    text = html_regex.sub("", text)

    # 处理转发/回复
    text = repost_regex.sub(" ", text)
    text = comment_regex.sub(" ", text)

    return text.strip(), tags, links
