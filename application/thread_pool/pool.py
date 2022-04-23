import typing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait

from config.flask_config import THREAD_MAX_COUNT

thread_executor = ThreadPoolExecutor(THREAD_MAX_COUNT)
process_executor = ProcessPoolExecutor(THREAD_MAX_COUNT)

__all__ = (
    "submit_function_async", "submit_function_with_waiting_result",
    "parallel_function_async", "parallel_function_with_waiting_result"
)


def submit_function_with_waiting_result(func: typing.Callable, *args, **kwargs):
    """
    分线程执行同步任务

    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    result = thread_executor.submit(func, *args, **kwargs)
    return result.result()


def submit_function_async(func: typing.Callable, *args, **kwargs):
    """
    分线程执行同步任务

    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    thread_executor.submit(func, *args, **kwargs)


def parallel_function_with_waiting_result(func: typing.Callable, iterables, timeout=None, chunk_size=8):
    """
    分线程执行同步任务

    :param func: 执行的函数
    :param iterables: 可迭代对象
    :param timeout: 超时时间
    :param chunk_size: 分块大小
    :return:
    """
    result = []
    futures = process_executor.map(func, iterables, timeout=timeout, chunksize=chunk_size)

    wait(futures)

    for future in futures:
        result.append(future.result())


def parallel_function_async(func: typing.Callable, iterables, timeout=None, chunk_size=8):
    """
    分线程执行同步任务

    :param func: 执行的函数
    :param iterables: 可迭代对象
    :param timeout: 超时时间
    :param chunk_size: 分块大小
    :return:
    """
    process_executor.map(func, iterables, timeout=timeout, chunksize=chunk_size)
