# encoding: utf-8
"""
@auth: cyq
@name: exception handling
@desc: 全局异常处理
"""


def handReturn(msg):
    return {
        "code": 1,
        "data": "",
        "msg": msg
    }


def catchError(func):
    def wrapper( *args, **kwargs):
        try:
            u = func( *args, **kwargs)
            return u
        except Exception as e:
            result = repr(e)
            return handReturn(result)

    return wrapper
