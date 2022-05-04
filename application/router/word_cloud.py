import json
import numpy

from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify

from config import Config
from libs import FormatLogger, map_sentiment_to_int_emotion, TagTrend

from .common import process_after_request, process_login_status
from ..functions import query_all_word_cloud, query_all_word_cloud_by_search_key
from ..functions import query_word_cloud_trend, query_word_cloud_trend_by_search_key
from ..functions import query_word_cloud_hot_trend, query_word_cloud_hot_trend_by_search_key

word_cloud_router = Blueprint("word_cloud", __name__)
word_cloud_router.before_request(process_login_status)
word_cloud_router.after_request(process_after_request)

__all__ = ("word_cloud_router",)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_cloud/all", methods=["POST"])
def request_word_cloud_all():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    response_data["data"]["config"] = {
        "color": {
            -1: Config.NEGATIVE_WORD_COLOR,
            0: Config.NEUTRAL_WORD_COLOR,
            1: Config.POSITIVE_WORD_COLOR,
        }
    }

    result = query_all_word_cloud(Config.SEARCH_KEYWORD, Config.WORD_CLOUD_LIMIT_COUNT)

    if result is None:
        response_data["status"] = 0
        response_data["message"] = "数据抓取成功"
    else:
        response_data["status"] = 0
        response_data["message"] = "数据抓取成功"
        response_data["data"]["word_cloud"] = []

        for item in result:
            response_data["data"]["word_cloud"].append({
                "key": item.key,
                "count": item.count,
                "emotion": map_sentiment_to_int_emotion(item.get_emotion())
            })

    return jsonify(response_data)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_cloud/search", methods=["POST"])
def request_word_cloud_search():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_keyword = request_json.get("Keyword", "")

    if request_keyword == "":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    response_data["data"]["config"] = {
        "color": {
            -1: Config.NEGATIVE_WORD_COLOR,
            0: Config.NEUTRAL_WORD_COLOR,
            1: Config.POSITIVE_WORD_COLOR,
        }
    }

    result = query_all_word_cloud_by_search_key(request_keyword, Config.WORD_CLOUD_LIMIT_COUNT)

    if result is None:
        response_data["status"] = 0
        response_data["message"] = "数据抓取成功"

    else:
        response_data["status"] = 0
        response_data["message"] = "数据抓取成功"
        response_data["data"]["word_cloud"] = []

        for item in result:
            response_data["data"]["word_cloud"].append({
                "key": item.key,
                "count": item.count,
                "emotion": map_sentiment_to_int_emotion(item.get_emotion())
            })

    return jsonify(response_data)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_trend/all", methods=["POST"])
def request_word_trend_all():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    result = query_word_cloud_trend(Config.SEARCH_KEYWORD)

    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"]["word_trend"] = {
        "decrease": [{"key": item.key, "value": item.count} for item in result["decrease"]],
        "increase": [{"key": item.key, "value": item.count} for item in result["increase"]],
    }

    return jsonify(response_data)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_trend/search", methods=["POST"])
def request_word_trend_search():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_keyword = request_json.get("Keyword", "")

    if request_keyword == "":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    result = query_word_cloud_trend_by_search_key(request_keyword)

    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"]["word_trend"] = {
        "decrease": [{"key": item.key, "value": item.count} for item in result["decrease"]],
        "increase": [{"key": item.key, "value": item.count} for item in result["increase"]],
    }

    return jsonify(response_data)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_hot_trend/all", methods=["POST"])
def request_word_hot_trend_all():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"]["word_hot_trend"] = []
    response_data["data"]["word_hot_trend_predict"] = []
    response_data["data"]["config"] = {
        "hour": Config.TREND_CYCLE_HOUR,
        "count": Config.TREND_CYCLE_COUNT
    }

    result: dict[datetime, TagTrend] = query_word_cloud_hot_trend(Config.SEARCH_KEYWORD)

    sort_list = sorted(result.items(), key=lambda item: item[0])

    predict_data = []
    for time, trend in sort_list:
        predict_data.append(trend.get_trend())
        response_data["data"]["word_hot_trend"].append({
            "time_point": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trend": trend.get_trend()
        })

    predict = predict_trend_1(predict_data)
    last_time = sort_list[-1][0]
    for index in range(len(predict)):
        time = last_time + timedelta(hours=Config.TREND_CYCLE_HOUR * (index + 1))
        response_data["data"]["word_hot_trend_predict"].append({
            "time_point": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trend": 0 if predict[index] < 0 else predict[index]
        })

    return jsonify(response_data)


# noinspection DuplicatedCode
@word_cloud_router.route("/api/word_hot_trend/search", methods=["POST"])
def request_word_hot_trend_search():
    """
    路由--请求爬虫更新

    :return:
    """
    response_data = {
        "status": -1,
        "message": "请求失败",
        "data": {}
    }

    if request.method != "POST":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    request_data = request.get_data()
    request_json = json.loads(request_data)
    request_keyword = request_json.get("Keyword", "")

    if request_keyword == "":
        FormatLogger.error("WordCloudRouter", "Error request method! Request url is {}".format(request.url))
        response_data["message"] = "无效请求"
        return jsonify(response_data)

    response_data["status"] = 0
    response_data["message"] = "数据抓取成功"
    response_data["data"]["word_hot_trend"] = []
    response_data["data"]["word_hot_trend_predict"] = []
    response_data["data"]["config"] = {
        "hour": Config.TREND_CYCLE_HOUR,
        "count": Config.TREND_CYCLE_COUNT
    }

    result = query_word_cloud_hot_trend_by_search_key(request_keyword)

    sort_list = sorted(result.items(), key=lambda item: item[0])

    predict_data = []
    for time, trend in sort_list:
        predict_data.append(trend.get_trend())
        response_data["data"]["word_hot_trend"].append({
            "time_point": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trend": trend.get_trend()
        })

    predict = predict_trend_1(predict_data)
    last_time = sort_list[-1][0]
    for index in range(len(predict)):
        time = last_time + timedelta(hours=Config.TREND_CYCLE_HOUR * (index + 1))
        response_data["data"]["word_hot_trend_predict"].append({
            "time_point": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trend": 0 if predict[index] < 0 else predict[index]
        })

    return jsonify(response_data)


def predict_trend_1(trend_data: list[float]):
    """
    热度值预测函数一

    多项式拟合

    :return:
    """
    x_axis = numpy.array([value for value in range(len(trend_data))])
    y_axis = numpy.array(trend_data)

    predict = numpy.poly1d(numpy.polyfit(x_axis, y_axis, 3))
    return [predict(len(trend_data)), predict(len(trend_data) + 1), predict(len(trend_data) + 2)]
