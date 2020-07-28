# encoding: utf-8
"""
@auth: cyq
@file: pwd.py
@desc: 测试用例接口
"""

import os


def get_cwd(filePath=None) -> str:
    path = os.path.dirname(__file__)
    if filePath:
        return path + f"/{filePath}"
    return path
