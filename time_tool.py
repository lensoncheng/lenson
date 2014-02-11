# -*- coding:utf8 -*-

import time
from functools import wraps


def timethis(func):
    """
    这是一个装饰器,计算一个函数的执行时间
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.process_time()
        r= func(*args, **kwargs)
        end = time.process_time()
        print "{}.{} : {}".format(func.__module__, func.__name__, end- start)
        return r
    return wrapper


"""
如果分析语句块的执行时间,那可以通过定义一个上下文管理器(context manager)
"""
from contextlib import contextmanager

@contextmanager
def timeblock(label):
    start = time.process_time()
    try:
        yield
    finally:
        end = time.process_time()
        print "{} : {}".format(label, end - start)

"""
具体使用的方法:
with timeblock('counting'):
    n = 10000
    while n > 0:
        n -= 1
"""
